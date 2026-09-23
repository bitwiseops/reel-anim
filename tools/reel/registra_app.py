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

from PIL import Image, ImageOps, ImageTk

from ..anim.config import Config
from . import clip as clipmod
from .cattura import Cattura, Microfono, Riproduttore
from .compositing import maschera_riquadro
from .ffmpeg import ffprobe
from .model import PIENO, Reel
from .registra import (PRESE, Karaoke, Presa, Timeline, carica_inquadratura, comando_cattura, comando_riproduzione, con_voce,
                       dimensioni_pipe, karaoke, limita_inquadratura, nuova_presa, prossima_presa, riquadro_in_scala,
                       salva_dispositivi_scelti, salva_inquadratura, snap_fotogramma, spezza)

TASTI = ("Spazio: registra / ferma   ·   P: prova senza registrare   ·   E: modifica il testo   ·   ← → o cifre: scena di partenza   ·   Esc: esci\n"
         "Inquadratura (prima di registrare): trascina il cerchio col mouse, rotella o + − per lo zoom, W A S D per spostarlo, 0 per il centro")
PAD = 16
RISERVA_ALTEZZA = 330      # prima stima di barra dei menu, titolo e comandi: poi si misura (`_adatta_allo_schermo`)
CORNICE_ALTEZZA = 70       # barra dei menu di macOS + titolo della finestra, che Tk non conta nella finestra
ALTO_MINIMO = 240          # sotto, i pannelli non servono più: meglio che la finestra sbordi
LARGHEZZA_KARAOKE = 520    # stretta e al centro, sotto la fotocamera: gli occhi si spostano poco (2026-09-23)
AIUTO_ERRORE = ("Controlla Impostazioni di Sistema → Privacy e sicurezza → Fotocamera e Microfono per l'app del terminale, "
                "che nessun'altra app usi la fotocamera, oppure scegli il dispositivo: `uv run reel registra --dispositivi`, `--video N`.")


class AppRegistra:
    def __init__(self, r: Reel, tl: Timeline, opz: dict, cfg: Config, cartella: Path, out: Path, avvisi: list[str],
                 da_scena: int | None = None, dispositivi: dict | None = None):
        self.r, self.tl, self.opz, self.cfg, self.cartella, self.out = r, tl, opz, cfg, cartella, out
        self.avvisi = avvisi
        self.dispositivi = dispositivi or {"video": [], "audio": []}   # {"video": [(indice, nome)], "audio": [...]}
        self.root = tk.Tk()        # prima dei pannelli: la loro misura dipende dallo schermo
        self.W, self.H = (int(x) for x in str(opz["risoluzione"]).lower().split("x"))
        self.lato_minimo = int(cfg.dati["riquadro"]["dimensione_px"])
        self.inq = carica_inquadratura(cartella, str(opz["risoluzione"]), self.lato_minimo)
        self._trascino: tuple[int, int, int, int] | None = None
        self._imposta_misure()
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
        self._adatta_allo_schermo()

    # --- finestra ----------------------------------------------------------------------------------

    def _imposta_misure(self, alto: int | None = None) -> None:
        """Pannelli e tutto ciò che ne dipende: scala del reel e della webcam, maschera del riquadro."""
        self.dim_webcam, self.dim_reel, self.dim_karaoke = self._misure_pannelli(alto)
        self.scala = self.dim_reel[0] / self.cfg.larghezza
        self.scala_webcam = self.dim_webcam[0] / self.W
        lato = riquadro_in_scala(self.cfg, "si", self.scala)[2]
        self.maschera = Image.open(maschera_riquadro(self.cfg)).convert("L").resize((lato, lato), Image.LANCZOS)

    def _adatta_allo_schermo(self) -> None:
        """La riserva per i comandi era una stima: qui si misura la finestra vera e, se sborda dallo schermo (in
        altezza o in larghezza), si rifanno i pannelli più bassi. Succede una volta, prima che partano le catture
        (2026-09-23: sul portatile i comandi finivano fuori schermo anche a tutto schermo)."""
        try:
            if self.opz.get("altezza_pannelli_px"):
                return
            self._restringi_allo_schermo()
        finally:
            self._centra_in_alto()

    def _centra_in_alto(self) -> None:
        """La finestra centrata in orizzontale e attaccata in alto: il karaoke, nella colonna centrale, cade sotto la
        fotocamera."""
        self.root.update_idletasks()
        x = max(0, (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2)
        self.root.geometry(f"+{x}+0")

    def _restringi_allo_schermo(self) -> None:
        for _ in range(3):
            self.root.update_idletasks()
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            troppo_alto = self.root.winfo_reqheight() + CORNICE_ALTEZZA - sh
            troppo_largo = self.root.winfo_reqwidth() - sw
            if troppo_alto <= 0 and troppo_largo <= 0:
                return
            alto = self.dim_karaoke[1]
            nuovo = alto - max(troppo_alto, 0)
            if troppo_largo > 0:     # i pannelli sono larghi in proporzione all'altezza: si stringono insieme
                nuovo = min(nuovo, int(alto * (sw - PAD * 2) / max(1, self.root.winfo_reqwidth())))
            nuovo = max(ALTO_MINIMO, nuovo - 4)
            if nuovo >= alto:
                return
            for figlio in self.root.winfo_children():
                figlio.destroy()
            self._imposta_misure(nuovo)
            self._costruisci_finestra()

    def _misure_pannelli(self, alto: int | None = None) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        """I tre pannelli stanno in fila sopra i comandi: prendono l'altezza che lo schermo lascia libera (o
        `altezza_pannelli_px`) e ognuno al massimo un terzo della larghezza. Webcam e reel tengono le proporzioni."""
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        alto = int(alto or self.opz.get("altezza_pannelli_px") or max(360, sh - RISERVA_ALTEZZA))
        larga_max = (sw - 4 * PAD) // 3

        def larghezza(w: int, h: int) -> int:
            return max(2, min(larga_max, round(w * alto / h)))

        W, H = (int(x) for x in str(self.opz["risoluzione"]).lower().split("x"))
        dim_webcam = dimensioni_pipe(f"{W}x{H}", larghezza(W, H))
        dim_reel = dimensioni_pipe(f"{self.cfg.larghezza}x{self.cfg.altezza}", larghezza(self.cfg.larghezza, self.cfg.altezza))
        alto = max(dim_webcam[1], dim_reel[1])
        larga_k = max(320, min(LARGHEZZA_KARAOKE, sw - dim_webcam[0] - dim_reel[0] - 5 * PAD))
        return dim_webcam, dim_reel, (larga_k, alto)

    def _costruisci_finestra(self) -> None:
        pal = self.cfg.palette
        self.colori = {"sfondo": pal.sfondo, "testo": pal.testo, "attenuato": pal.attenuato, "accento": pal.accento,
                       "secondario": pal.secondario, "rec": "#E0524D"}
        root = self.root
        root.title(f"reel registra · {self.r.meta.get('titolo', self.r.slug)}")
        root.configure(bg=pal.sfondo)
        root.resizable(False, False)
        famiglia = "Helvetica Neue" if "Helvetica Neue" in tkfont.families() else "Helvetica"
        lk, alto = self.dim_karaoke
        corpo = max(18, min(30, alto // 22))
        self.f_karaoke = tkfont.Font(family=famiglia, size=corpo)
        self.f_karaoke_b = tkfont.Font(family=famiglia, size=corpo, weight="bold")
        self.f_piccolo = tkfont.Font(family=famiglia, size=13)
        self.f_piccolo_editor = tkfont.Font(family=famiglia, size=max(16, corpo * 2 // 3))
        self.f_medio = tkfont.Font(family=famiglia, size=16, weight="bold")
        self.f_conto = tkfont.Font(family=famiglia, size=max(60, self.dim_reel[0] // 3), weight="bold")

        # sopra: i tre pannelli in fila, alti uguali
        pannelli = tk.Frame(root, bg=pal.sfondo)
        pannelli.grid(row=0, column=0, sticky="w", padx=PAD, pady=(PAD, 8))
        w, h = self.dim_webcam
        self.c_webcam = tk.Canvas(pannelli, width=w, height=h, bg="black", highlightthickness=0)
        self.c_webcam.grid(row=0, column=0, sticky="n")
        self.foto_webcam = ImageTk.PhotoImage(Image.new("RGB", self.dim_webcam, (0, 0, 0)))
        self.c_webcam.create_image(0, 0, anchor="nw", image=self.foto_webcam)
        self.g_quadrato = self.c_webcam.create_rectangle(0, 0, 1, 1, outline=pal.attenuato, dash=(4, 4))
        self.g_cerchio = self.c_webcam.create_oval(0, 0, 1, 1, outline=pal.accento, width=2)
        self._disegna_guida()
        self.c_webcam.bind("<ButtonPress-1>", self._inizio_trascino)
        self.c_webcam.bind("<B1-Motion>", self._trascina)
        self.c_webcam.bind("<MouseWheel>", lambda e: self._zoom(-1 if e.delta > 0 else 1))

        w, h = self.dim_reel
        self.c_reel = tk.Canvas(pannelli, width=w, height=h, bg="black", highlightthickness=0)
        self.c_reel.grid(row=0, column=2, sticky="n")
        self.foto_reel = ImageTk.PhotoImage(Image.new("RGB", self.dim_reel, (0, 0, 0)))
        self.c_reel.create_image(0, 0, anchor="nw", image=self.foto_reel)
        self.t_conto = self.c_reel.create_text(w // 2, h // 2, text="", font=self.f_conto, fill=pal.accento)
        self.t_rec = self.c_reel.create_text(w - 14, 16, text="", font=self.f_medio, fill=self.colori["rec"], anchor="ne")

        # il karaoke al centro, fra webcam e reel: con la finestra centrata in alto sta subito sotto la fotocamera del
        # portatile, e leggendo lo sguardo resta in camera (il presentatore, 2026-09-23)
        dx = tk.Frame(pannelli, bg=pal.sfondo, width=lk, height=alto)
        dx.grid(row=0, column=1, sticky="n", padx=PAD)
        dx.pack_propagate(False)
        self.l_intestazione = tk.Label(dx, text="", font=self.f_medio, fg=pal.attenuato, bg=pal.sfondo, anchor="w")
        self.l_intestazione.pack(fill="x")
        self.larga_barra = lk
        self.c_barra = tk.Canvas(dx, width=lk, height=6, bg=pal.sfondo, highlightthickness=0)
        self.c_barra.pack(fill="x", pady=(4, 12))
        self.barra = self.c_barra.create_rectangle(0, 0, 0, 6, fill=pal.accento, outline="")
        self.t_karaoke = tk.Text(dx, wrap="word", font=self.f_karaoke, bg=pal.sfondo, fg=pal.testo,
                                 bd=0, highlightthickness=0, padx=4, pady=4, cursor="arrow", spacing1=6, spacing3=6)
        self.t_karaoke.pack(fill="both", expand=True)
        self.t_karaoke.tag_configure("attenuata", foreground=pal.attenuato)
        self.t_karaoke.tag_configure("corrente", foreground=pal.testo)
        self.t_karaoke.tag_configure("accesa", foreground=pal.accento, font=self.f_karaoke_b)
        self.t_karaoke.tag_configure("nota", foreground=pal.secondario, font=self.f_piccolo)
        self.t_karaoke.configure(state="disabled")
        larghezza_totale = self.dim_webcam[0] + self.dim_reel[0] + lk + 2 * PAD

        # sotto: le scene, i comandi di registrazione e riproduzione, i dispositivi, lo stato
        comandi = tk.Frame(root, bg=pal.sfondo)
        comandi.grid(row=1, column=0, sticky="we", padx=PAD, pady=(0, PAD))
        riga_scene = tk.Frame(comandi, bg=pal.sfondo)
        riga_scene.pack(fill="x")
        self.l_scene: list[tk.Label] = []
        for s in self.tl.scene:
            lbl = tk.Label(riga_scene, font=self.f_piccolo, bg=pal.sfondo, fg=pal.testo, justify="left", padx=8, pady=2, cursor="hand2")
            lbl.pack(side="left", padx=(0, 4))
            lbl.bind("<Button-1>", lambda e, n=s.n: self._scegli_scena(n))
            self.l_scene.append(lbl)

        riga = tk.Frame(comandi, bg=pal.sfondo)
        riga.pack(fill="x", pady=(8, 4))
        self.b_registra = ttk.Button(riga, text="● Registra  (Spazio)", takefocus=False, command=self._clic(self._spazio))
        self.b_prova = ttk.Button(riga, text="▶ Prova senza registrare  (P)", takefocus=False, command=self._clic(self._prova))
        self.b_ferma = ttk.Button(riga, text="■ Ferma", takefocus=False, command=self._clic(self._ferma))
        self.b_prima = ttk.Button(riga, text="◀ Scena", takefocus=False, command=self._clic(lambda: self._cambia_scena(-1)))
        self.b_dopo = ttk.Button(riga, text="Scena ▶", takefocus=False, command=self._clic(lambda: self._cambia_scena(+1)))
        self.b_modifica = ttk.Button(riga, text="✎ Modifica testo  (E)", takefocus=False, command=self._modifica_o_salva)
        self.b_annulla = ttk.Button(riga, text="Annulla  (Esc)", takefocus=False, command=self._clic(self._annulla_modifica))
        for b in (self.b_registra, self.b_prova, self.b_ferma, self.b_prima, self.b_dopo, self.b_modifica, self.b_annulla):
            b.pack(side="left", padx=(0, 6))
        # i menu dei dispositivi su una riga loro: con i pulsanti sulla stessa riga uscivano dallo schermo del portatile
        riga = tk.Frame(comandi, bg=pal.sfondo)
        riga.pack(fill="x", pady=(0, 4))
        self.menu_dispositivi: dict[str, ttk.Combobox] = {}
        for tipo, etichetta in (("audio", "Microfono"), ("video", "Fotocamera")):
            voci = [f"[{i}] {n}" for i, n in self.dispositivi[tipo]]
            if tipo == "audio":
                voci.insert(0, "predefinito di sistema")
            cb = ttk.Combobox(riga, values=voci, state="readonly", font=self.f_piccolo, width=24)
            tk.Label(riga, text=etichetta, font=self.f_piccolo, fg=pal.attenuato, bg=pal.sfondo).pack(side="left", padx=(0, 4))
            cb.pack(side="left", padx=(0, 16))
            cb.bind("<<ComboboxSelected>>", lambda e, t=tipo: self._scegli_dispositivo(t))
            # col fuoco sul menu: Spazio registra (non apre il menu), Esc lascia il menu (non chiude l'app)
            cb.bind("<space>", lambda e: (self.root.focus_set(), self._spazio(), "break")[-1])
            cb.bind("<Escape>", lambda e: (self.root.focus_set(), "break")[-1])
            self.menu_dispositivi[tipo] = cb
            self._mostra_dispositivo(tipo)

        self.l_stato = tk.Label(comandi, text="", font=self.f_medio, fg=pal.testo, bg=pal.sfondo, anchor="nw",
                                wraplength=larghezza_totale, justify="left", height=2)   # alta fissa: un messaggio lungo
                                                                                          # non deve spingere giù la finestra
        self.l_stato.pack(fill="x", pady=(4, 0))
        tk.Label(comandi, text="Il cerchio sulla webcam è ciò che va nel riquadro: volto al centro, spazio sopra la testa.\n" + TASTI,
                 font=self.f_piccolo, fg=pal.attenuato, bg=pal.sfondo, anchor="w", justify="left").pack(fill="x", pady=(4, 0))

        root.bind_all("<space>", lambda e: self._spazio())
        root.bind_all("<Left>", lambda e: self._cambia_scena(-1))
        root.bind_all("<Right>", lambda e: self._cambia_scena(+1))
        root.bind_all("<Key>", self._tasto)
        root.bind_all("<Escape>", lambda e: self._esc())
        root.protocol("WM_DELETE_WINDOW", self._esc)
        root.focus_set()

    def _clic(self, azione):
        """Un pulsante non tiene il fuoco: dopo il clic Spazio e le frecce tornano alla finestra."""
        def f():
            azione()
            self.root.focus_set()
        return f

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
        if self._menu_aperto() or self.stato == "modifica":     # nel testo Spazio è uno spazio
            return
        if self.stato == "pronto":
            self._avvia_presa()
        elif self.stato == "presa":
            self._ferma_presa("stop")
        elif self.stato in ("apertura", "conto"):
            self._annulla_presa("presa annullata")
        elif self.stato == "prova":
            self._ferma_prova("prova fermata")
        elif self.stato == "errore":
            self.stato = "pronto"
            self.messaggio = ""
            self._avvia_anteprima()
            self._mostra_fermo()

    def _ferma(self) -> None:
        """Il pulsante ■: ferma la presa o la prova, annulla il conto alla rovescia."""
        if self.stato in ("presa", "apertura", "conto", "prova"):
            self._spazio()

    def _scegli_scena(self, n: int) -> None:
        if self.stato == "pronto":
            self.da_scena = n
            self._disegna_elenco()
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
        if self.stato == "prova" and e.char and e.char.lower() == "e":
            self._apri_modifica()
            return
        if self.stato != "pronto" or not e.char:
            return
        c = e.char.lower()
        if c == "p":
            self._prova()
        elif c == "e":
            self._apri_modifica()
        elif c.isdigit() and int(c) in [s.n for s in self.tl.scene]:
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
        if self.stato == "modifica":
            self._annulla_modifica()
            return
        if self.stato == "prova":
            self._ferma_prova("")
            return
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

    # --- prova senza registrare --------------------------------------------------------------------

    def _prova(self) -> None:
        """Il reel dalla scena scelta con il volto live e il karaoke, come in una presa, ma niente file e niente
        microfono: per provare il ritmo della lettura. L'anteprima della webcam resta quella di sempre."""
        if self.stato != "pronto" or self._menu_aperto():
            return
        self.t_reel0 = self.tl.scena_n(self.da_scena).t_inizio_s - float(self.opz["preroll_s"])
        t0 = snap_fotogramma(self.t_reel0, self.tl.fps)
        self.riproduttore = Riproduttore(comando_riproduzione(self.tl.reel, t0, self.dim_reel), self.dim_reel, t0, self.tl.fps)
        self.riproduttore.avvia()
        self.T0 = time.monotonic()
        self.stato = "prova"
        self.messaggio = ""

    def _ferma_prova(self, messaggio: str) -> None:
        if self.riproduttore:
            self.riproduttore.ferma()
            self.riproduttore = None
        self.stato = "pronto"
        self.messaggio = messaggio
        self._mostra_fermo()

    # --- il testo si corregge qui (fuori dalla presa) ---------------------------------------------------
    # Il pannello del karaoke diventa modificabile con le righe della scena scelta, una per frase. Al salvataggio
    # le righe vanno in contenuti/media/<slug>/parlato.json e nella timeline: la presa dopo le mostra nel karaoke e
    # le scrive nel sidecar, e il montaggio ne fa le caption.

    def _modifica_o_salva(self) -> None:
        self._salva_modifica() if self.stato == "modifica" else self._apri_modifica()

    def _apri_modifica(self) -> None:
        if self.stato == "prova":
            scena = self.tl.scena_a(self.t_reel0 + (time.monotonic() - self.T0))
            self._ferma_prova("")
            if scena is not None:
                self.da_scena = scena.n
        if self.stato != "pronto" or self._menu_aperto():
            return
        s = self.tl.scena_n(self.da_scena)
        self.stato = "modifica"
        self.messaggio = ""
        t = self.t_karaoke
        t.configure(state="normal", cursor="xterm", font=self.f_piccolo_editor)
        t.delete("1.0", "end")
        t.insert("1.0", "\n".join(f.grezzo or f.testo for f in s.frasi))
        t.bind("<Command-Return>", lambda e: (self._salva_modifica(), "break")[-1])
        t.focus_set()
        self._disegna_elenco()

    def _chiudi_editor(self) -> None:
        t = self.t_karaoke
        t.unbind("<Command-Return>")
        t.configure(state="disabled", cursor="arrow", font=self.f_karaoke)
        self._chiave_karaoke = None
        self.stato = "pronto"
        self.root.focus_set()
        self._disegna_elenco()
        self._mostra_fermo()

    def _salva_modifica(self) -> None:
        if self.stato != "modifica":
            return
        n = self.da_scena
        righe = [x.strip() for x in self.t_karaoke.get("1.0", "end").split("\n") if x.strip()]
        attese = len(self.tl.scena_n(n).frasi)
        if len(righe) != attese:
            self.messaggio = (f"scena {n}: servono {attese} righe, una per frase (ne hai scritte {len(righe)}): "
                              "i beat dell'animazione sono legati alle frasi")
            return
        voce_md = list(self.r.scena(n).voce) if self.r.scena(n) else []
        clipmod.salva_parlato(self.r.slug, n, None if righe == voce_md else righe)
        self.tl = con_voce(self.tl, n, righe)
        self._chiudi_editor()
        self.messaggio = f"testo della scena {n} salvato" + (" (è tornato quello della sceneggiatura)" if righe == voce_md else "")

    def _annulla_modifica(self) -> None:
        if self.stato == "modifica":
            self._chiudi_editor()
            self.messaggio = "modifica annullata"

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
        if self.stato == "prova":
            t = self.t_reel0 + (adesso - self.T0)
            fr = self.riproduttore.prossimo_fino_a(t)
            scena = self.tl.scena_a(t)
            if fr is not None:
                self.foto_reel.paste(self._componi(fr, webcam[1] if webcam else None, scena))
            self._disegna_karaoke(karaoke(self.tl, t))
            self.messaggio = (f"▶ PROVA (non registra) · reel {max(0.0, t):.1f} s / {self.tl.durata_s:.1f} s"
                              + (f" · scena {scena.n}/{len(self.tl.scene)}" if scena else " · pre-roll")
                              + "   —   Spazio o ■ per fermare")
            if t >= self.tl.durata_s:
                self._ferma_prova("prova finita")
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
        if webcam_rgb and scena and scena.riquadro == PIENO:
            # a volto pieno la tela è lui: la webcam intera, riempita e ritagliata al centro, come farà il montaggio
            return ImageOps.fit(Image.frombytes("RGB", self.dim_webcam, webcam_rgb), self.dim_reel, Image.BILINEAR)
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
        if self.stato == "modifica":
            return
        principale = k.frase or k.prossima
        chiave = (id(k.scena), id(principale), k.accese, id(k.precedente), round(k.attesa_s, 1) if k.attesa_s > 0.5 else 0, pronto)
        if k.scena:
            self.l_intestazione.configure(text=f"Scena {k.scena.n}/{len(self.tl.scene)} · {k.scena.tipo}")
        else:
            self.l_intestazione.configure(text="Prima del reel")
        self.c_barra.coords(self.barra, 0, 0, int(self.larga_barra * k.frazione_scena), 6)
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
        cambiate = clipmod.carica_parlato(self.r.slug)
        for lbl, s in zip(self.l_scene, self.tl.scene):
            c = clipmod.trova(self.r.slug, s.n)
            presa = ""
            for p in self.prese_fatte:
                if s.n in p.scene:
                    presa = f" · {p.nome}"
            segno = "✔" if c else "✘"
            lbl.configure(text=f"{segno} scena {s.n:02d}{' ✎' if s.n in cambiate else ''}{presa}\n{s.tipo} · {s.durata_s:.1f} s",
                          fg=pal["testo"] if c else pal["attenuato"],
                          bg=pal["secondario"] if s.n == self.da_scena else pal["sfondo"])

    def _disegna_stato(self) -> None:
        if self.stato == "modifica":
            n = self.da_scena
            testo = (f"✎ Testo della scena {n}: una riga per frase ({len(self.tl.scena_n(n).frasi)} righe), ==parola== per "
                     "l'evidenza nelle caption.   ⌘↩ salva · Esc annulla") + (f"\n{self.messaggio}" if self.messaggio else "")
        elif self.stato == "pronto" and not self.messaggio:
            testo = f"Pronto · Spazio registra dalla scena {self.da_scena} (parte {self.opz['preroll_s']:.0f} s prima, dopo il conto alla rovescia)"
        elif self.stato == "pronto":
            testo = self.messaggio + f"   —   Spazio registra dalla scena {self.da_scena}"
        else:
            testo = self.messaggio
        if self.avvisi and self.stato == "pronto":
            testo += "\n⚠ " + " · ".join(self.avvisi)
        self.l_stato.configure(text=testo, fg=self.colori["rec"] if self.stato in ("errore", "presa") else self.colori["testo"])
        pronto = self.stato == "pronto"
        self.b_registra.configure(text="● Registra  (Spazio)" if self.stato != "errore" else "↻ Riprova  (Spazio)",
                                  state="normal" if self.stato in ("pronto", "errore") else "disabled")
        for b in (self.b_prova, self.b_prima, self.b_dopo):
            b.configure(state="normal" if pronto else "disabled")
        self.b_ferma.configure(state="normal" if self.stato in ("presa", "apertura", "conto", "prova") else "disabled")
        modifica = self.stato == "modifica"
        self.b_modifica.configure(text="✔ Salva testo  (⌘↩)" if modifica else "✎ Modifica testo  (E)",
                                  state="normal" if self.stato in ("pronto", "prova", "modifica") else "disabled")
        self.b_annulla.configure(state="normal" if modifica else "disabled")

    @staticmethod
    def _mmss(s: float) -> str:
        return f"{int(s // 60):02d}:{s % 60:04.1f}"
