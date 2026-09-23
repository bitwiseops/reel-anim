"""Processi ffmpeg letti da un thread, senza Tk: la webcam (slot «ultimo fotogramma», che non blocca mai) e il reel
(coda limitata: la contropressione su un file è innocua); il microfono con PortAudio (`sounddevice`), scritto in un
wav da un thread. Si prova con una sorgente lavfi al posto della webcam."""
from __future__ import annotations

import queue
import signal
import subprocess
import threading
import wave
from pathlib import Path


class Livello:
    """Il vu-meter della registrazione: uno stream d'ingresso a parte, acceso anche fuori dalla presa (il volume
    d'ingresso si regola prima), che tiene il picco con una discesa lenta come un vu-meter vero. Non scrive niente."""

    CADUTA_DB_S = 15.0

    def __init__(self, dispositivo: int | str | None, frequenza: int = 48000):
        self.dispositivo, self.frequenza = dispositivo, frequenza
        self._lock = threading.Lock()
        self._picco, self._t = -90.0, 0.0
        self.massimo = -90.0          # il picco più alto da quando è acceso: dice se ha saturato
        self.stream = None
        self.errore = ""

    def avvia(self) -> None:
        import sounddevice as sd
        try:
            self.stream = sd.InputStream(device=self.dispositivo, samplerate=self.frequenza, channels=1, dtype="int16",
                                         blocksize=1024, callback=self._callback)
            self.stream.start()
        except Exception as e:  # noqa: BLE001 — senza vu-meter si registra lo stesso
            self.errore, self.stream = str(e), None

    def _callback(self, indata, frames, tempo, stato) -> None:
        import time
        from .registra import dbfs
        db = dbfs(int(abs(indata).max()) if frames else 0)
        adesso = time.monotonic()
        with self._lock:
            if db >= self._valore(adesso):
                self._picco, self._t = db, adesso
            self.massimo = max(self.massimo, db)

    def _valore(self, adesso: float) -> float:
        return max(-90.0, self._picco - self.CADUTA_DB_S * max(0.0, adesso - self._t))

    def picco_db(self) -> float:
        import time
        with self._lock:
            return self._valore(time.monotonic())

    def ferma(self) -> None:
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:  # noqa: BLE001
                pass
            self.stream = None


class Microfono:
    """Registra il microfono in un wav (PCM 16 bit mono). `n` conta i campioni consegnati dal callback: con la latenza
    d'ingresso riferita da PortAudio dà l'istante nel wav di qualunque istante del clock di Python."""

    def __init__(self, dispositivo: int | str | None, frequenza: int, dest: Path):
        self.dispositivo, self.frequenza, self.dest = dispositivo, frequenza, dest
        self._lock = threading.Lock()
        self._n = 0
        self.anomalie = 0            # overflow o altri stati segnalati da PortAudio
        self.latenza_s = 0.0
        self._coda: queue.Queue = queue.Queue()
        self._thread: threading.Thread | None = None
        self.stream = None
        self.errore = ""

    def avvia(self) -> None:
        import sounddevice as sd
        self.dest.parent.mkdir(parents=True, exist_ok=True)
        self._wav = wave.open(str(self.dest), "wb")
        self._wav.setnchannels(1)
        self._wav.setsampwidth(2)
        self._wav.setframerate(self.frequenza)
        self._thread = threading.Thread(target=self._scrivi, name="microfono", daemon=True)
        self._thread.start()
        self.stream = sd.InputStream(device=self.dispositivo, samplerate=self.frequenza, channels=1, dtype="int16",
                                     latency="low", callback=self._callback)
        self.stream.start()
        self.latenza_s = float(self.stream.latency)

    def _callback(self, indata, frames, tempo, stato) -> None:
        if stato:
            self.anomalie += 1
        with self._lock:
            self._n += frames
        self._coda.put(indata.tobytes())

    def _scrivi(self) -> None:
        while True:
            b = self._coda.get()
            if b is None:
                self._wav.close()
                return
            self._wav.writeframes(b)

    @property
    def n(self) -> int:
        with self._lock:
            return self._n

    def vivo(self) -> bool:
        return self.stream is not None and bool(self.stream.active)

    def ferma(self) -> int:
        """Chiude lo stream e il wav; ritorna il numero di stati anomali segnalati."""
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:  # noqa: BLE001 — PortAudio può lamentarsi alla chiusura: il wav conta di più
                self.errore = str(e)
            self.stream = None
        if self._thread is not None:
            self._coda.put(None)
            self._thread.join(5.0)
            self._thread = None
        return self.anomalie


class Cattura:
    """Un ffmpeg con i fotogrammi rgb24 su stdout. Il thread lettore drena sempre la pipe: se si fermasse, ffmpeg si
    bloccherebbe sulla write e avfoundation scarterebbe audio e video alla sorgente (buchi nella presa)."""

    def __init__(self, cmd: list[str], dim: tuple[int, int], log: Path):
        self.cmd, self.dim, self.log = cmd, dim, log
        self.proc: subprocess.Popen | None = None
        self._lock = threading.Lock()
        self._k = 0
        self._ultimo: bytes | None = None
        self._fine = False
        self._thread: threading.Thread | None = None
        self._log_f = None

    def avvia(self) -> None:
        self.log.parent.mkdir(parents=True, exist_ok=True)
        self._log_f = open(self.log, "w", encoding="utf-8")
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self._log_f, bufsize=0)
        self._thread = threading.Thread(target=self._leggi, name="cattura", daemon=True)
        self._thread.start()

    def _leggi(self) -> None:
        n = self.dim[0] * self.dim[1] * 3
        out = self.proc.stdout
        while True:
            buf = bytearray(n)
            vista = memoryview(buf)
            letti = 0
            while letti < n:
                r = out.readinto(vista[letti:])
                if not r:
                    self._fine = True
                    return
                letti += r
            with self._lock:
                self._k += 1
                self._ultimo = bytes(buf)

    @property
    def k(self) -> int:
        with self._lock:
            return self._k

    def ultimo(self) -> tuple[int, bytes] | None:
        with self._lock:
            return (self._k, self._ultimo) if self._ultimo is not None else None

    def vivo(self) -> bool:
        return self.proc is not None and self.proc.poll() is None and not self._fine

    def ferma(self, timeout_s: float = 6.0) -> int:
        """`q` sullo stdin chiude gli encoder e scrive il moov; poi SIGINT; kill solo come ultima risorsa."""
        p = self.proc
        if p is None:
            return -1
        if p.poll() is None:
            try:
                p.stdin.write(b"q\n")
                p.stdin.flush()
            except (BrokenPipeError, OSError):
                pass
            try:
                p.wait(timeout_s)
            except subprocess.TimeoutExpired:
                p.send_signal(signal.SIGINT)
                try:
                    p.wait(timeout_s)
                except subprocess.TimeoutExpired:
                    p.kill()
                    p.wait()
        if self._thread:
            self._thread.join(timeout_s)
        for f in (p.stdin, p.stdout, self._log_f):
            try:
                f.close()
            except (OSError, AttributeError):
                pass
        return p.returncode

    def errore(self) -> str:
        """La coda del log di ffmpeg, per capire perché è morto."""
        try:
            righe = self.log.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return ""
        return "\n".join(righe[-20:])


class Riproduttore:
    """ffmpeg che decodifica il reel da t0_s: il fotogramma k della pipe è l'istante t0_s + k/fps. Chi disegna chiede
    `prossimo_fino_a(t)` e riceve l'ultimo fotogramma non oltre t (scartando quelli in ritardo)."""

    def __init__(self, cmd: list[str], dim: tuple[int, int], t0_s: float, fps: int, coda: int = 8):
        self.cmd, self.dim, self.t0_s, self.fps = cmd, dim, t0_s, fps
        self._coda: queue.Queue = queue.Queue(maxsize=coda)
        self.proc: subprocess.Popen | None = None
        self._thread: threading.Thread | None = None
        self._in_attesa: tuple[float, bytes] | None = None
        self._corrente: bytes | None = None
        self.finito = False

    def avvia(self) -> None:
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
        self._thread = threading.Thread(target=self._leggi, name="riproduttore", daemon=True)
        self._thread.start()

    def _leggi(self) -> None:
        n = self.dim[0] * self.dim[1] * 3
        out = self.proc.stdout
        k = 0
        while True:
            buf = bytearray(n)
            vista = memoryview(buf)
            letti = 0
            while letti < n:
                r = out.readinto(vista[letti:])
                if not r:
                    self._coda.put(None)
                    return
                letti += r
            self._coda.put((self.t0_s + k / self.fps, bytes(buf)))
            k += 1

    def prossimo_fino_a(self, t: float) -> bytes | None:
        while True:
            if self._in_attesa is None:
                try:
                    x = self._coda.get_nowait()
                except queue.Empty:
                    break
                if x is None:
                    self.finito = True
                    break
                self._in_attesa = x
            if self._in_attesa[0] <= t:
                self._corrente = self._in_attesa[1]
                self._in_attesa = None
            else:
                break
        return self._corrente

    def ferma(self) -> None:
        p = self.proc
        if p is not None and p.poll() is None:
            p.kill()
            p.wait()
        if p is not None:
            try:
                p.stdout.close()
            except OSError:
                pass
