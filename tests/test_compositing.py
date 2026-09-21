"""I comandi ffmpeg costruiti come liste di stringhe (senza eseguirli): filtergraph, posizioni, codifica, concat."""
from pathlib import Path

from tools.anim.config import carica
from tools.reel.compositing import Sorgenti, comando_concat, comando_scena, durata_concat, posizione_riquadro

GRAFICA = Path("/tmp/grafica.mp4")
DEST = Path("/tmp/scena.mp4")


def _filtri(cmd: list[str]) -> str:
    return cmd[cmd.index("-filter_complex") + 1]


def test_posizioni_del_riquadro():
    cfg = carica()
    assert posizione_riquadro(cfg, "si") == posizione_riquadro(cfg, "alto-destra") == (576, 220, 360)
    assert posizione_riquadro(cfg, "basso-destra") == (576, 1220, 360)
    assert posizione_riquadro(cfg, "basso-sinistra") == (84, 1220, 360)
    assert posizione_riquadro(cfg, "alto-sinistra") == (84, 220, 360)


def test_scena_senza_riquadro_con_voce_sintetica_in_anteprima():
    cmd = comando_scena(Sorgenti(GRAFICA, 4.0, "no", audio=Path("/tmp/voce.m4a")), DEST, anteprima=True)
    f = _filtri(cmd)
    assert "scale=1080:1920" in f and "alphamerge" not in f and "aresample=48000,apad[a]" in f
    assert cmd[cmd.index("-t") + 1] == "4.000" and "ultrafast" in cmd
    assert cmd[cmd.index("-ac") + 1] == "2"   # stereo anche con la voce mono


def test_scena_con_avatar_nel_riquadro():
    cmd = comando_scena(Sorgenti(GRAFICA, 5.0, "alto-destra", avatar=Path("/tmp/avatar.png")), DEST)
    f = _filtri(cmd)
    assert "alphamerge" in f and "crop=360:360" in f and "overlay=x=576:y=220" in f
    assert "anullsrc=r=48000:cl=stereo" in cmd and cmd[cmd.index("-crf") + 1] == "18"


def test_scena_con_la_clip_del_presentatore():
    f = _filtri(comando_scena(Sorgenti(GRAFICA, 5.0, "si", video_presentatore=Path("/tmp/scena-02.mov")), DEST))
    assert "loudnorm=I=-16" in f and "overlay=x=576:y=220" in f   # «si» = alto-destra, sopra la fascia delle caption


def test_scena_schermo_con_broll():
    sc = carica().dati["schermo"]
    cmd = comando_scena(Sorgenti(Path("/tmp/grafica.mov"), 6.0, "alto-destra", avatar=Path("/tmp/avatar.png"),
                                 schermo=Path("/tmp/chat.png")), DEST)
    f = _filtri(cmd)
    assert f"crop={sc['larghezza']}:{sc['altezza']}" in f and f"overlay=x={sc['x']}:y={sc['y']}" in f
    assert "format=rgba[gr]" in f and any(a.startswith("color=c=") for a in cmd)


def test_concat_con_dissolvenza_e_con_taglio():
    pezzi = [(Path("/tmp/1.mp4"), 4.0), (Path("/tmp/2.mp4"), 8.0), (Path("/tmp/3.mp4"), 6.0)]
    f = _filtri(comando_concat(pezzi, Path("/tmp/reel.mp4"), "dissolvenza", 0.25))
    assert "offset=3.750" in f and "offset=11.500" in f and f.count("acrossfade") == 2
    assert durata_concat(pezzi, "dissolvenza", 0.25) == 17.5
    assert "concat=n=3:v=1:a=1" in _filtri(comando_concat(pezzi, Path("/tmp/reel.mp4"), "taglio"))
    cmd = comando_concat(pezzi, Path("/tmp/reel.mp4"), "dissolvenza", 0.25)
    assert cmd[cmd.index("-ac") + 1] == "2"
    assert durata_concat(pezzi, "taglio", 0.25) == 18.0


def test_scena_broll_il_filmato_riempie_la_tela_senza_cornice():
    """[broll]: il filmato è il livello di base a tutta tela, col riquadro sopra; niente finestra, niente sfondo."""
    cfg = carica()
    cmd = comando_scena(Sorgenti(Path("/tmp/broll-scena-04.mp4"), 9.0, "si", avatar=Path("/tmp/avatar.png"),
                                 audio=Path("/tmp/voce.m4a"), filmato=True), DEST)
    f = _filtri(cmd)
    assert f"force_original_aspect_ratio=increase:flags=lanczos,crop={cfg.larghezza}:{cfg.altezza},fps={cfg.fps}" in f
    assert "[v0][pipA]overlay" in f                                   # il presentatore sopra il filmato è voluto
    assert "mskS" not in f and not any(a.startswith("color=c=") for a in cmd)
    assert "-stream_loop" not in cmd                                  # un filmato corto non si ripete: lo dice `monta`
    # un'immagine ferma (immagini composte messe a mano) va tenuta aperta per tutta la scena
    ferma = comando_scena(Sorgenti(Path("/tmp/foto.png"), 9.0, "no", filmato=True), DEST)
    i = ferma.index("/tmp/foto.png")
    assert ferma[i - 5: i] == ["-loop", "1", "-t", "9.000", "-i"]   # un'immagine ferma: in loop, ma finita


def test_concat_con_un_taglio_verso_il_filmato_dentro_una_dissolvenza():
    """Fra animazione e filmato si stacca; il resto del reel resta in dissolvenza."""
    pezzi = [(Path(f"/tmp/{k}.mp4"), 6.0) for k in range(4)]
    f = _filtri(comando_concat(pezzi, Path("/tmp/reel.mp4"), "dissolvenza", 0.25, tagli=frozenset({1, 2})))
    assert "[n0][0:a][n1][1:a]concat=n=2:v=1:a=1[c1][a1]" in f and "[v1][a1][n2][2:a]concat" in f
    assert "[v2][n3]xfade=transition=fade:duration=0.25:offset=17.750[v3]" in f       # 6 + 6 + 6 − 0,25
    assert f.count("settb=AVTB") == 4 + 2                     # ogni ingresso e ogni uscita di concat, per xfade
    assert durata_concat(pezzi, "dissolvenza", 0.25, frozenset({1, 2})) == 23.75
    assert "settb" not in _filtri(comando_concat(pezzi, Path("/tmp/reel.mp4"), "dissolvenza", 0.25))   # senza tagli, come sempre


def test_copertina_dell_hook_a_filmato_porta_il_titolo(tmp_path):
    """A schermo il titolo non c'è: la copertina lo scrive sopra il fotogramma, dentro la banda 4:5."""
    from PIL import Image

    from tools.reel.fotogrammi import ritaglio_4x5, titola

    cfg = carica()
    f = tmp_path / "copertina.png"
    Image.new("RGB", (cfg.larghezza, cfg.altezza), (240, 240, 240)).save(f)
    titola(f, "Chiedi una mail all'IA", "E ti arriva ==quella di tutti==", cfg)
    im = Image.open(f).convert("RGB")
    _, alto, _, basso = ritaglio_4x5(cfg)
    scritti = [(x, y) for x in range(0, cfg.larghezza, 4) for y in range(0, cfg.altezza, 4)
               if im.getpixel((x, y)) != im.getpixel((2, 2))]
    assert scritti and all(alto <= y <= basso for _, y in scritti)                  # tutto dentro il ritaglio 4:5
    assert max(x for x, _ in scritti) < cfg.larghezza - 60                           # e dentro il margine destro
    accento = tuple(int(cfg.palette.accento[i:i + 2], 16) for i in (1, 3, 5))
    assert any(im.getpixel(p) == accento for p in scritti)                           # il sottotitolo in accento


def test_volto_pieno_il_presentatore_e_la_tela():
    """Apertura e chiusura (dal 2026-09-21): la clip riempie 1080×1920 e la grafica, trasparente, gli va sopra."""
    clip = Path("/tmp/scena-09.mov")
    f = _filtri(comando_scena(Sorgenti(Path("/tmp/grafica.mov"), 6.0, "pieno", video_presentatore=clip), DEST))
    assert "scale=1080:1920:force_original_aspect_ratio=increase" in f and "crop=1080:1920" in f
    assert "[volto][gr]overlay=0:0" in f and "alphamerge" not in f     # niente cerchio: non c'è riquadro
    assert "loudnorm" in f                                              # l'audio resta quello della clip
    solo = _filtri(comando_scena(Sorgenti(None, 5.0, "pieno", video_presentatore=clip), DEST))
    assert "[volto]null[v0]" in solo and "[gr]" not in solo            # l'apertura: lui e basta


def test_ogni_immagine_in_loop_ha_una_durata():
    """Senza `-t` un `-loop 1` è infinito e ffmpeg 8.1 a volte non chiude (2026-09-21)."""
    cmd = comando_scena(Sorgenti(GRAFICA, 5.0, "si", avatar=Path("/tmp/avatar.png"),
                                 caption=((Path("/tmp/c0.png"), 0.0, 2.0),), caption_xy=(0, 1500)), DEST)
    loop = [i for i, a in enumerate(cmd) if a == "-loop"]
    assert loop and all(cmd[i + 2: i + 4] == ["-t", "5.000"] for i in loop)


def test_le_caption_entrano_come_fotogramma_singolo():
    """Una caption per blocco, in loop, portava una scena lunga a 13 ingressi infiniti e ffmpeg 8.1 andava in stallo
    (2026-09-21): ora ognuna è un fotogramma solo che l'overlay ripete."""
    caps = tuple((Path(f"/tmp/c{k}.png"), k * 1.0, k * 1.0 + 0.9) for k in range(11))
    cmd = comando_scena(Sorgenti(GRAFICA, 12.0, "si", avatar=Path("/tmp/avatar.png"), caption=caps, caption_xy=(0, 1500)),
                        DEST)
    for png, _, _ in caps:
        i = cmd.index(str(png))
        assert cmd[i - 1] == "-i" and cmd[i - 2] != "18.0" and "-loop" not in cmd[i - 5: i]
    assert _filtri(cmd).count("eof_action=repeat") == 11
    assert cmd.count("-loop") == 2                      # restano solo avatar e maschera del cerchio
