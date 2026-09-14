"""La finestra di `reel registra` (Tkinter): webcam con la guida del cerchio, l'anteprima del reel con il volto live
nel riquadro, il testo karaoke. Solo il main thread tocca Tk: i processi ffmpeg li leggono i thread di `cattura`,
la spezzatura gira in un thread e riferisce con `root.after`."""
from __future__ import annotations

import math
import queue
import sys
import threading
import time
import tkinter as tk
import traceback
from pathlib import Path
from tkinter import font as tkfont
from tkinter import ttk

from PIL import Image, ImageTk

from ..anim.config import Config
from . import clip as clipmod
from .cattura import Cattura, Microfono, Riproduttore
from .compositing import maschera_riquadro
from .ffmpeg import ffprobe
from .model import Reel
from .registra import (PRESE, Karaoke, Presa, Timeline, carica_inquadratura, comando_cattura, comando_riproduzione,
                       dimensioni_pipe, karaoke, limita_inquadratura, nuova_presa, prossima_presa, riquadro_in_scala,
                       salva_dispositivi_scelti, salva_inquadratura, snap_fotogramma, spezza)

TASTI = ("Spazio: registra / ferma   ·   ← → o cifre: scena di partenza   ·   Esc: esci\n"
         "Inquadratura (prima di registrare): trascina il cerchio col mouse, rotella o + − per lo zoom, W A S D per spostarlo, 0 per il centro")
AIUTO_ERRORE = ("Controlla Impostazioni di Sistema → Privacy e sicurezza → Fotocamera e Microfono per l'app del terminale, "
                "che nessun'altra app usi la fotocamera, oppure scegli il dispositivo: `uv run reel registra --dispositivi`, `--video N`.")


class AppRegistra:
    def __init__(self, r: Reel, tl: Timeline, opz: dict, cfg: Config, cartella: Path, out: Path, avvisi: list[str],
                 da_scena: int | None = None, dispositivi: dict | None = None):
        self.r, self.tl, self.opz, self.cfg, self.cartella, self.out = r, tl, opz, cfg, cartella, out
        self.avvisi = avvisi
        self.dispositivi = dispositivi or {"video": [], "audio": []}   # {"video": [(indice, nome)], "audio": [...]}
        self.dim_webcam = dimensioni_pipe(str(opz["risoluzione"]), int(opz["anteprima_webcam_px"]))
        self.dim_reel = dimensioni_pipe(f"{cfg.larghezza}x{cfg.altezza}", int(opz["anteprima_reel_px"]))
        self.scala = self.dim_reel[0] / cfg.larghezza
        self.W, self.H = (int(x) for x in str(opz["risoluzione"]).lower().split("x"))
        self.scala_webcam = self.dim_webcam[0] / self.W
        self.lato_minimo = int(cfg.dati["riquadro"]["dimensione_px"])
        self.inq = carica_inquadratura(cartella, str(opz["risoluzione"]), self.lato_minimo)
        self._trascino: tuple[int, int, int, int] | None = None
        lato = riquadro_in_scala(cfg, "si", self.scala)[2]
        self.maschera = Image.open(maschera_riquadro(cfg)).convert("L").resize((lato, lato), Image.LANCZOS)
        self.stato = "pronto"
        self.messaggio = ""
        self.anteprima: Cattura | None = None
        self.cattura: Cattura | None = None
        self.mic: Microfono | None = None
        self.riproduttore: Riproduttore | None = None
        self.presa: Presa | None = None
        self.nome_presa = ""
        self.t_reel0 = 0.0
        self.T0 = 0.0
        self.k0 = 0
        self.n0 = 0
        self.t_apertura = 0.0
        self.conto_fine = 0.0
        self.chiudi_dopo = False
        self.prese_fatte: list[Presa] = []
        self._eventi: queue.Queue = queue.Queue()   # dal thread di spezzatura al main thread (solo il main thread tocca Tk)
        self._fermi: dict[int, Image.Image] = {}
        self._chiave_karaoke = None
        self.da_scena = da_scena or self._prima_senza_clip()
        self._costruisci_finestra()

    # --- finestra ----------------------------------------------------------------------------------

    def _costruisci_finestra(self) -> None:
        pal = self.cfg.palette
        self.colori = {"sfondo": pal.sfondo, "testo": pal.testo, "attenuato": pal.attenuato, "accento": pal.accento,
                       "secondario": pal.secondario, "rec": "#E0524D"}
        root = self.root = tk.Tk()
        root.title(f"reel registra · {self.r.meta.get('titolo', self.r.slug)}")
        root.configure(bg=pal.sfondo)
        root.resizable(False, False)
        famiglia = "Helvetica Neue" if "Helvetica Neue" in tkfont.families() else "Helvetica"
        self.f_karaoke = tkfont.Font(family=famiglia, size=30)
        self.f_karaoke_b = tkfont.Font(family=famiglia, size=30, weight="bold")
        self.f_piccolo = tkfont.Font(family=famiglia, size=14)
        self.f_medio = tkfont.Font(family=famiglia, size=17, weight="bold")
        self.f_conto = tkfont.Font(family=famiglia, size=120, weight="bold")
        pad = 16

        # sinistra: webcam + elenco scene
        sx = tk.Frame(root, bg=pal.sfondo)
        sx.grid(row=0, column=0, sticky="n", padx=(pad, 0), pady=pad)
        w, h = self.dim_webcam
        self.c_webcam = tk.Canvas(sx, width=w, height=h, bg="black", highlightthickness=0)
        self.c_webcam.pack()
        self.foto_webcam = ImageTk.PhotoImage(Image.new("RGB", self.dim_webcam, (0, 0, 0)))
        self.c_webcam.create_image(0, 0, anchor="nw", image=self.foto_webcam)
        self.g_quadrato = self.c_webcam.create_rectangle(0, 0, 1, 1, outline=pal.attenuato, dash=(4, 4))
        self.g_cerchio = self.c_webcam.create_oval(0, 0, 1, 1, outline=pal.accento, width=2)
        self._disegna_guida()
        self.c_webcam.bind("<ButtonPress-1>", self._inizio_trascino)
        self.c_webcam.bind("<B1-Motion>", self._trascina)
        self.c_webcam.bind("<MouseWheel>", lambda e: self._zoom(-1 if e.delta > 0 else 1))
        tk.Label(sx, text="Il cerchio è ciò che va nel riquadro: volto al centro, spazio sopra la testa.", font=self.f_piccolo,
                 fg=pal.attenuato, bg=pal.sfondo, wraplength=w, justify="left").pack(anchor="w", pady=(6, 8))
        self.menu_dispositivi: dict[str, ttk.Combobox] = {}
        for tipo, etichetta in (("video", "Fotocamera"), ("audio", "Microfono")):
            riga = tk.Frame(sx, bg=pal.sfondo)
            riga.pack(fill="x", pady=(0, 4))
            tk.Label(riga, text=etichetta, font=self.f_piccolo, fg=pal.attenuato, bg=pal.sfondo, width=11, anchor="w").pack(side="left")
            voci = [f"[{i}] {n}" for i, n in self.dispositivi[tipo]]
            if tipo == "audio":
                voci.insert(0, "predefinito di sistema")
            cb = ttk.Combobox(riga, values=voci, state="readonly", font=self.f_piccolo, width=34)
            cb.pack(side="left", fill="x", expand=True)
            cb.bind("<<ComboboxSelected>>", lambda e, t=tipo: self._scegli_dispositivo(t))
            # col fuoco sul menu: Spazio registra (non apre il menu), Esc lascia il menu (non chiude l'app)
            cb.bind("<space>", lambda e: (self.root.focus_set(), self._spazio(), "break")[-1])
            cb.bind("<Escape>", lambda e: (self.root.focus_set(), "break")[-1])
            self.menu_dispositivi[tipo] = cb
            self._mostra_dispositivo(tipo)
        tk.Frame(sx, bg=pal.sfondo, height=8).pack()
        self.l_scene: list[tk.Label] = []
        for _ in self.tl.scene:
            lbl = tk.Label(sx, font=self.f_piccolo, bg=pal.sfondo, fg=pal.testo, anchor="w", padx=8)
            lbl.pack(fill="x")
            self.l_scene.append(lbl)

        # centro: il reel con il volto live
        w, h = self.dim_reel
        self.c_reel = tk.Canvas(root, width=w, height=h, bg="black", highlightthickness=0)
        self.c_reel.grid(row=0, column=1, padx=pad, pady=pad)
        self.foto_reel = ImageTk.PhotoImage(Image.new("RGB", self.dim_reel, (0, 0, 0)))
        self.c_reel.create_image(0, 0, anchor="nw", image=self.foto_reel)
        self.t_conto = self.c_reel.create_text(w // 2, h // 2, text="", font=self.f_conto, fill=pal.accento)
        self.t_rec = self.c_reel.create_text(w - 14, 16, text="", font=self.f_medio, fill=self.colori["rec"], anchor="ne")

        # destra: karaoke
        dx = tk.Frame(root, bg=pal.sfondo, width=560)
        dx.grid(row=0, column=2, sticky="n", padx=(0, pad), pady=pad)
        self.l_intestazione = tk.Label(dx, text="", font=self.f_medio, fg=pal.attenuato, bg=pal.sfondo, anchor="w")
        self.l_intestazione.pack(fill="x")
        self.c_barra = tk.Canvas(dx, width=560, height=6, bg=pal.sfondo, highlightthickness=0)
        self.c_barra.pack(fill="x", pady=(4, 12))
        self.barra = self.c_barra.create_rectangle(0, 0, 0, 6, fill=pal.accento, outline="")
        self.t_karaoke = tk.Text(dx, width=26, height=13, wrap="word", font=self.f_karaoke, bg=pal.sfondo, fg=pal.testo,
                                 bd=0, highlightthickness=0, padx=4, pady=4, cursor="arrow", spacing1=6, spacing3=6)
        self.t_karaoke.pack(fill="both")
        self.t_karaoke.tag_configure("attenuata", foreground=pal.attenuato)
        self.t_karaoke.tag_configure("corrente", foreground=pal.testo)
        self.t_karaoke.tag_configure("accesa", foreground=pal.accento, font=self.f_karaoke_b)
        self.t_karaoke.tag_configure("nota", foreground=pal.secondario, font=self.f_piccolo)
        self.t_karaoke.configure(state="disabled")

        # in basso: stato e tasti
        self.l_stato = tk.Label(root, text="", font=self.f_medio, fg=pal.testo, bg=pal.sfondo, anchor="w", wraplength=1400, justify="left")
        self.l_stato.grid(row=1, column=0, columnspan=3, sticky="we", padx=pad)
        tk.Label(root, text=TASTI, font=self.f_piccolo, fg=pal.attenuato, bg=pal.sfondo, anchor="w").grid(
            row=2, column=0, columnspan=3, sticky="we", padx=pad, pady=(4, pad))

        root.bind_all("<space>", lambda e: self._spazio())
        root.bind_all("<Left>", lambda e: self._cambia_scena(-1))
        root.bind_all("<Right>", lambda e: self._cambia_scena(+1))
        root.bind_all("<Key>", self._tasto)
        root.bind_all("<Escape>", lambda e: self._esc())
        root.protocol("WM_DELETE_WINDOW", self._esc)
        root.focus_set()

    def esegui(self) -> int:
        self._avvia_anteprima()
        self._disegna_elenco()
        self._mostra_fermo()
        self.root.after(1000 // int(self.opz["fps_pannelli"]), self._tick)
        self.root.mainloop()
        return 0

    # --- stato -------------------------------------------------------------------------------------

    def _prima_senza_clip(self) -> int:
        for s in self.tl.scene:
            if clipmod.trova(self.r.slug, s.n) is None:
                return s.n
        return self.tl.scene[0].n

    def _log(self, nome: str) -> Path:
        return self.cartella / PRESE / f"{nome}.log"

    def _avvia_anteprima(self) -> None:
        # opz["sorgente"]: argomenti ffmpeg al posto della webcam (test con lavfi)
        self.anteprima = Cattura(comando_cattura(self.opz, None, self.dim_webcam, self.opz.get("sorgente")), self.dim_webcam, self._log("anteprima"))
        self.anteprima.avvia()

    def _sorgente_webcam(self) -> Cattura | None:
        return self.cattura or self.anteprima

    def _menu_aperto(self) -> bool:
        """Il fuoco è sulla tendina aperta di un menu (un widget interno di Tk che Tkinter non conosce: focus_get() fallisce)."""
        try:
            return "popdown" in str(self.root.tk.call("focus"))
        except tk.TclError:
            return False

    def _spazio(self) -> None:
        if self._menu_aperto():
            return
        if self.stato == "pronto":
            self._avvia_presa()
        elif self.stato == "presa":
            self._ferma_presa("stop")
        elif self.stato in ("apertura", "conto"):
            self._annulla_presa("presa annullata")
        elif self.stato == "errore":
            self.stato = "pronto"
            self.messaggio = ""
            self._avvia_anteprima()
            self._mostra_fermo()

    def _cambia_scena(self, delta: int) -> None:
        if self.stato != "pronto":
            return
        i = self.tl.indice(self.da_scena) + delta
        if 0 <= i < len(self.tl.scene):
            self.da_scena = self.tl.scene[i].n
            self._disegna_elenco()
            self._mostra_fermo()

    def _tasto(self, e) -> None:
        if self.stato != "pronto" or not e.char:
            return
        c = e.char.lower()
        if c.isdigit() and int(c) in [s.n for s in self.tl.scene]:
            self.da_scena = int(c)
            self._disegna_elenco()
            self._mostra_fermo()
        elif c in ("+", "="):
            self._zoom(-1)
        elif c == "-":
            self._zoom(+1)
        elif c in ("w", "a", "s", "d"):
            passo = max(8, self.inq["lato"] // 20)
            dx, dy = {"w": (0, -passo), "s": (0, passo), "a": (-passo, 0), "d": (passo, 0)}[c]
            self._imposta_inquadratura({**self.inq, "x": self.inq["x"] + dx, "y": self.inq["y"] + dy})
        elif c == "0":
            self._imposta_inquadratura({"lato": min(self.W, self.H), "x": 0, "y": 0}, centra=True)

    # --- dispositivi ---------------------------------------------------------------------------------

    def _mostra_dispositivo(self, tipo: str) -> None:
        cb = self.menu_dispositivi[tipo]
        scelto = self.opz.get(tipo)
        voce = "predefinito di sistema" if scelto is None else next((f"[{i}] {n}" for i, n in self.dispositivi[tipo] if i == scelto), "")
        if voce:
            cb.set(voce)

    def _scegli_dispositivo(self, tipo: str) -> None:
        cb = self.menu_dispositivi[tipo]
        self.root.focus_set()          # altrimenti Spazio riapre il menu invece di registrare
        if self.stato != "pronto":
            self._mostra_dispositivo(tipo)
            return
        voce = cb.get()
        if voce == "predefinito di sistema":
            indice, nome = None, ""
        else:
            indice = int(voce[1:voce.index("]")])
            nome = dict(self.dispositivi[tipo]).get(indice, "")
        if indice == self.opz.get(tipo):
            return
        self.opz[tipo] = indice
        salva_dispositivi_scelti({tipo: nome})
        self.messaggio = f"{'fotocamera' if tipo == 'video' else 'microfono'}: {nome or 'predefinito di sistema'}"
        if tipo == "video":
            if self.anteprima:
                self.anteprima.ferma()
            self._avvia_anteprima()

    # --- inquadratura --------------------------------------------------------------------------------

    def _imposta_inquadratura(self, inq: dict, centra: bool = False) -> None:
        if centra:
            inq = {"lato": inq["lato"], "x": (self.W - inq["lato"]) // 2, "y": (self.H - inq["lato"]) // 2}
        nuova = limita_inquadratura(inq, str(self.opz["risoluzione"]), self.lato_minimo)
        if nuova != self.inq:
            self.inq = nuova
            salva_inquadratura(self.cartella, self.inq)
            self._disegna_guida()

    def _zoom(self, verso: int) -> None:
        """verso −1 = avvicina (quadrato più piccolo), +1 = allarga; il centro resta dov'è."""
        if self.stato != "pronto":
            return
        passo = max(8, self.inq["lato"] // 12) * verso
        lato = self.inq["lato"] + passo
        cx, cy = self.inq["x"] + self.inq["lato"] / 2, self.inq["y"] + self.inq["lato"] / 2
        self._imposta_inquadratura({"lato": lato, "x": round(cx - lato / 2), "y": round(cy - lato / 2)})

    def _inizio_trascino(self, e) -> None:
        self._trascino = (e.x, e.y, self.inq["x"], self.inq["y"])

    def _trascina(self, e) -> None:
        if self.stato != "pronto" or not self._trascino:
            return
        x0, y0, qx, qy = self._trascino
        s = self.scala_webcam
        self._imposta_inquadratura({**self.inq, "x": round(qx + (e.x - x0) / s), "y": round(qy + (e.y - y0) / s)})

    def _disegna_guida(self) -> None:
        s = self.scala_webcam
        x, y, lato = self.inq["x"] * s, self.inq["y"] * s, self.inq["lato"] * s
        self.c_webcam.coords(self.g_quadrato, x, y, x + lato - 1, y + lato - 1)
        self.c_webcam.coords(self.g_cerchio, x, y, x + lato - 1, y + lato - 1)

    def _esc(self) -> None:
        if self._menu_aperto():
            return                     # Esc chiude la tendina, non l'app
        if self.stato == "presa":
            self.chiudi_dopo = True
            self._ferma_presa("esc")
        elif self.stato == "spezzo":
            self.chiudi_dopo = True
        else:
            if self.stato in ("apertura", "conto"):
                self._annulla_presa("")
            self._chiudi()

    def _ferma_mic(self) -> int:
        anomalie = self.mic.ferma() if self.mic else 0
        self.mic = None
        return anomalie

    def _chiudi(self) -> None:
        for p in (self.cattura, self.anteprima):
            if p:
                p.ferma()
        self.cattura = self.anteprima = None
        self._ferma_mic()
        if self.riproduttore:
            self.riproduttore.ferma()
            self.riproduttore = None
        if self.root.winfo_exists():
            self.root.destroy()

    def _avvia_presa(self) -> None:
        if self.anteprima:
            self.anteprima.ferma()
            self.anteprima = None
        self.nome_presa = prossima_presa(self.cartella)
        file = self.cartella / PRESE / f"{self.nome_presa}.mov"
        self.cattura = Cattura(comando_cattura(self.opz, file, self.dim_webcam, self.opz.get("sorgente")), self.dim_webcam, self._log(self.nome_presa))
        self.cattura.avvia()
        self.mic = Microfono(self.opz["audio"], int(self.opz["frequenza_audio"]), file.with_suffix(".wav"))
        try:
            self.mic.avvia()
        except Exception as e:  # noqa: BLE001 — PortAudio: dispositivo assente, occupato o permesso negato
            self.mic = None
            self._errore(f"microfono non disponibile ({type(e).__name__}: {e}).")
            return
        self.t_reel0 = self.tl.scena_n(self.da_scena).t_inizio_s - float(self.opz["preroll_s"])
        t0 = snap_fotogramma(self.t_reel0, self.tl.fps)
        self.riproduttore = Riproduttore(comando_riproduzione(self.tl.reel, t0, self.dim_reel), self.dim_reel, t0, self.tl.fps)
        self.riproduttore.avvia()
        self.stato = "apertura"
        self.t_apertura = time.monotonic()
        self.messaggio = "In attesa della fotocamera… se macOS chiede il permesso, concedilo."

    def _annulla_presa(self, messaggio: str) -> None:
        self._ferma_mic()
        if self.cattura:
            self.cattura.ferma()
            file = self.cartella / PRESE / f"{self.nome_presa}.mov"
            file.unlink(missing_ok=True)
            file.with_suffix(".wav").unlink(missing_ok=True)
            self.cattura = None
        if self.riproduttore:
            self.riproduttore.ferma()
            self.riproduttore = None
        self.stato = "pronto"
        self.messaggio = messaggio
        self._avvia_anteprima()
        self._mostra_fermo()

    def _errore(self, messaggio: str) -> None:
        coda = self.cattura.errore() if self.cattura else ""
        self._ferma_mic()
        if self.cattura:
            self.cattura.ferma()
            self.cattura = None
        if self.anteprima:
            self.anteprima.ferma()
            self.anteprima = None
        if self.riproduttore:
            self.riproduttore.ferma()
            self.riproduttore = None
        self.stato = "errore"
        self.messaggio = f"{messaggio}\n{AIUTO_ERRORE}" + (f"\n{coda}" if coda else "") + "\nSpazio per riprovare, Esc per uscire."
        print(f"errore: {messaggio}\n{coda}", file=sys.stderr)

    def _ferma_presa(self, motivo: str) -> None:
        t_stop = self.t_reel0 + (time.monotonic() - self.T0)
        self.riproduttore.ferma()
        self.riproduttore = None
        latenza_audio = self.mic.latenza_s if self.mic else 0.0
        anomalie = self._ferma_mic()
        rc = self.cattura.ferma()
        coda = self.cattura.errore()
        self.cattura = None
        file = self.cartella / PRESE / f"{self.nome_presa}.mov"
        pr = ffprobe(file) if file.exists() else {"errore": "file assente"}
        if rc != 0 or "errore" in pr or not pr.get("durata_s"):
            self.stato = "errore"
            self.messaggio = f"la presa {self.nome_presa} non è leggibile (ffmpeg {rc}): scartata.\n{coda}\nSpazio per riprovare, Esc per uscire."
            return
        self.presa = nuova_presa(self.nome_presa, self.da_scena, self.t_reel0, self.k0, float(pr.get("inizio_video_s") or 0),
                                 self.opz, t_stop, self.tl.hash_md, n0=self.n0, latenza_audio_s=latenza_audio, inquadratura=self.inq)
        self.stato = "spezzo"
        self.messaggio = f"{self.nome_presa}: {pr['durata_s']:.1f} s registrati, taglio le scene…"
        if anomalie:
            print(f"{self.nome_presa}: PortAudio ha segnalato {anomalie} anomalie (overflow?) sull'audio", file=sys.stderr)
        threading.Thread(target=self._spezza, args=(self.presa,), daemon=True).start()

    def _spezza(self, p: Presa) -> None:
        def avanzamento(i, n, s):
            self._eventi.put(("messaggio", f"{p.nome}: taglio la scena {s.n} ({i + 1}/{n})…"))
        try:
            fatte = spezza(self.tl, p, self.cartella, self.opz, avanzamento)
            self._eventi.put(("fine", p, fatte, None))
        except Exception as e:  # noqa: BLE001 — l'errore va mostrato nella finestra, non deve uccidere il thread in silenzio
            self._eventi.put(("fine", p, [], f"{type(e).__name__}: {e}"))

    def _svuota_eventi(self) -> None:
        while True:
            try:
                ev = self._eventi.get_nowait()
            except queue.Empty:
                return
            if ev[0] == "messaggio":
                self.messaggio = ev[1]
            elif ev[0] == "fine":
                self._dopo_spezzatura(*ev[1:])

    def _dopo_spezzatura(self, p: Presa, fatte: list[Path], errore: str | None) -> None:
        self.prese_fatte.append(p)
        if errore:
            self.messaggio = f"{p.nome}: taglio fallito ({errore}). La presa è nel registro: `uv run reel registra <file> --spezza {p.nome}`."
        elif fatte:
            self.messaggio = f"{p.nome}: salvate le scene {', '.join(str(n) for n in p.scene)} in contenuti/media/{self.r.slug}/."
        else:
            self.messaggio = f"{p.nome}: nessuna scena completa (fermata prima della fine della scena {p.da_scena})."
        print(self.messaggio, file=sys.stderr)
        if self.chiudi_dopo:
            self._chiudi()
            return
        self.stato = "pronto"
        self.da_scena = self._prima_senza_clip() if fatte else self.da_scena
        self._avvia_anteprima()
        self._disegna_elenco()
        self._mostra_fermo()

    # --- disegno -----------------------------------------------------------------------------------

    def _tick(self) -> None:
        try:
            self._aggiorna()
        except Exception:  # noqa: BLE001 — un errore di disegno non deve fermare il ciclo
            traceback.print_exc()
        if self.root.winfo_exists():
            self.root.after(1000 // int(self.opz["fps_pannelli"]), self._tick)

    def _aggiorna(self) -> None:
        adesso = time.monotonic()
        self._svuota_eventi()
        if not self.root.winfo_exists():
            return
        src = self._sorgente_webcam()
        webcam = src.ultimo() if src else None
        if webcam:
            self.foto_webcam.paste(Image.frombytes("RGB", self.dim_webcam, webcam[1]))
        if src and not src.vivo() and self.stato in ("apertura", "conto", "presa"):
            self._errore(f"ffmpeg si è fermato durante la {self.stato}.")
        elif src and not src.vivo() and self.stato == "pronto" and src is self.anteprima:
            self._errore("l'anteprima della fotocamera si è fermata.")

        if self.stato == "apertura":
            if src and src.k >= 1:
                self.stato = "conto"
                self.conto_fine = adesso + float(self.opz["conto_alla_rovescia_s"])
                self.messaggio = ""
            elif adesso - self.t_apertura > float(self.opz["timeout_apertura_s"]):
                self._errore("nessun fotogramma dalla fotocamera.")
        if self.stato == "conto":
            resto = self.conto_fine - adesso
            if resto <= 0:
                self.T0 = adesso
                self.k0 = src.k
                self.n0 = self.mic.n if self.mic else 0
                self.stato = "presa"
                self.c_reel.itemconfig(self.t_conto, text="")
            else:
                self.c_reel.itemconfig(self.t_conto, text=str(math.ceil(resto)))
        if self.stato == "presa":
            t = self.t_reel0 + (adesso - self.T0)
            fr = self.riproduttore.prossimo_fino_a(t)
            scena = self.tl.scena_a(t)
            if fr is not None:
                self.foto_reel.paste(self._componi(fr, webcam[1] if webcam else None, scena))
            self._disegna_karaoke(karaoke(self.tl, t))
            self.c_reel.itemconfig(self.t_rec, text="● REC" if int(adesso * 2) % 2 else "   REC")
            self.messaggio = (f"● REC {self._mmss(adesso - self.T0)} · reel {max(0.0, t):.1f} s / {self.tl.durata_s:.1f} s"
                              + (f" · scena {scena.n}/{len(self.tl.scene)}" if scena else " · pre-roll"))
            if t >= self.tl.durata_s + float(self.opz["coda_presa_s"]):
                self._ferma_presa("fine")
        else:
            self.c_reel.itemconfig(self.t_rec, text="")
        self._disegna_stato()

    def _componi(self, reel_rgb: bytes, webcam_rgb: bytes | None, scena) -> Image.Image:
        im = Image.frombytes("RGB", self.dim_reel, reel_rgb)
        if webcam_rgb and scena and scena.riquadro != "no":
            x, y, lato = riquadro_in_scala(self.cfg, scena.riquadro, self.scala)
            w = Image.frombytes("RGB", self.dim_webcam, webcam_rgb)
            s = self.scala_webcam
            x0, y0, q = round(self.inq["x"] * s), round(self.inq["y"] * s), max(1, round(self.inq["lato"] * s))
            volto = w.crop((x0, y0, x0 + q, y0 + q)).resize((lato, lato), Image.BILINEAR)
            im.paste(volto, (x, y), self.maschera)
        return im

    def _mostra_fermo(self) -> None:
        """In attesa: il fotogramma chiave della scena di partenza e la sua prima frase."""
        n = self.da_scena
        if n not in self._fermi:
            p = self.out / "scene" / f"{n:02d}.png"
            self._fermi[n] = Image.open(p).convert("RGB").resize(self.dim_reel, Image.LANCZOS) if p.exists() else Image.new("RGB", self.dim_reel, (0, 0, 0))
        self.foto_reel.paste(self._fermi[n])
        self.c_reel.itemconfig(self.t_conto, text="")
        s = self.tl.scena_n(n)
        self._disegna_karaoke(Karaoke(s, None, 0, 0.0, None, s.frasi[0] if s.frasi else None, 0.0), pronto=True)

    def _disegna_karaoke(self, k: Karaoke, pronto: bool = False) -> None:
        principale = k.frase or k.prossima
        chiave = (id(k.scena), id(principale), k.accese, id(k.precedente), round(k.attesa_s, 1) if k.attesa_s > 0.5 else 0, pronto)
        if k.scena:
            self.l_intestazione.configure(text=f"Scena {k.scena.n}/{len(self.tl.scene)} · {k.scena.tipo}")
        else:
            self.l_intestazione.configure(text="Prima del reel")
        self.c_barra.coords(self.barra, 0, 0, int(560 * k.frazione_scena), 6)
        if chiave == self._chiave_karaoke:
            return
        self._chiave_karaoke = chiave
        frasi = self.tl.frasi
        dopo = None
        if principale is not None and principale in frasi:
            i = frasi.index(principale)
            dopo = frasi[i + 1] if i + 1 < len(frasi) else None
        t = self.t_karaoke
        t.configure(state="normal")
        t.delete("1.0", "end")
        if k.precedente is not None:
            t.insert("end", k.precedente.testo + "\n\n", "attenuata")
        if principale is None:
            t.insert("end", "(fine del reel)\n", "attenuata")
        else:
            if pronto:
                t.insert("end", "Spazio per registrare da qui\n", "nota")
            elif k.frase is None and k.attesa_s > 0.5:
                t.insert("end", f"fra {k.attesa_s:.1f} s\n", "nota")
            for i, p in enumerate(principale.parole):
                t.insert("end", p + (" " if i + 1 < len(principale.parole) else ""), "accesa" if i < k.accese else "corrente")
            t.insert("end", "\n\n")
        if dopo is not None:
            t.insert("end", dopo.testo + "\n", "attenuata")
        t.configure(state="disabled")

    def _disegna_elenco(self) -> None:
        pal = self.colori
        for lbl, s in zip(self.l_scene, self.tl.scene):
            c = clipmod.trova(self.r.slug, s.n)
            presa = ""
            for p in self.prese_fatte:
                if s.n in p.scene:
                    presa = f" · {p.nome}"
            segno = "✔" if c else "✘"
            lbl.configure(text=f"{segno}  scena {s.n:02d}  {s.tipo:<12} {s.durata_s:5.1f} s{presa}",
                          fg=pal["testo"] if c else pal["attenuato"],
                          bg=pal["secondario"] if s.n == self.da_scena else pal["sfondo"])

    def _disegna_stato(self) -> None:
        if self.stato == "pronto" and not self.messaggio:
            testo = f"Pronto · Spazio registra dalla scena {self.da_scena} (parte {self.opz['preroll_s']:.0f} s prima, dopo il conto alla rovescia)"
        elif self.stato == "pronto":
            testo = self.messaggio + f"   —   Spazio registra dalla scena {self.da_scena}"
        else:
            testo = self.messaggio
        if self.avvisi and self.stato == "pronto":
            testo += "\n⚠ " + " · ".join(self.avvisi)
        self.l_stato.configure(text=testo, fg=self.colori["rec"] if self.stato in ("errore", "presa") else self.colori["testo"])

    @staticmethod
    def _mmss(s: float) -> str:
        return f"{int(s // 60):02d}:{s % 60:04.1f}"
