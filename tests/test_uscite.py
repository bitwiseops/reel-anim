import json
import threading
from pathlib import Path

import pytest

from tools.anim.config import Config
from tools.reel import uscite
from tools.reel.uscite import (ErroreUscite, Richiesta, Uscita, anonimizza, comando, componi, estrai_result, genera, richieste,
                               riga_uscite, scrivi_file, segnalazioni, sigle, slug_e_data, termini_account)

IDEA = """# Un'idea

**Data:** 2026-09-19
**Stato:** idea

## Note per il reel

- **A · questo non conta:** `sta prima dell'intestazione`

**Testi del modello: richieste da generare (T0b).** Una richiesta per riga:

- **A · base («migliora»):** `Migliora questa mail. «Buongiorno signora Carla, le sedie arrivano venerdì.»`
- **B · errore comune (+ «mantenendo il mio stile»):** `Migliora questa mail mantenendo il mio stile.
  «Buongiorno signora Carla,
  le sedie arrivano venerdì.»`
- **C · con un backtick dentro:** ``Spiegami `ls` in una riga.``

**Cosa cercare nelle uscite**
- A: quante frasi tornano identiche.

## Domande

- **D · fuori dalle note:** `non si legge`
"""


def test_richieste_dall_idea_anche_su_piu_righe():
    rr = richieste(IDEA)
    assert [(r.sigla, r.nome) for r in rr] == [("A", "base («migliora»)"), ("B", "errore comune (+ «mantenendo il mio stile»)"),
                                               ("C", "con un backtick dentro")]
    assert rr[0].testo == "Migliora questa mail. «Buongiorno signora Carla, le sedie arrivano venerdì.»"
    assert rr[1].testo == "Migliora questa mail mantenendo il mio stile. «Buongiorno signora Carla, le sedie arrivano venerdì.»"
    assert rr[2].testo == "Spiegami `ls` in una riga."


def test_richieste_assenti_o_fuori_ordine():
    with pytest.raises(ErroreUscite, match="Testi del modello"):
        richieste("# Idea\n\n## Note per il reel\n\nNiente da generare.\n")
    with pytest.raises(ErroreUscite, match="nessuna richiesta"):
        richieste("## Note per il reel\n\n**Testi del modello: richieste da generare (T0b).** **Nessuna.**\n")
    with pytest.raises(ErroreUscite, match="fuori ordine"):
        richieste(IDEA.replace("- **B · errore", "- **C · errore"))


def test_idee_vere_del_repo():
    idee = Path(__file__).resolve().parents[1] / "contenuti" / "idee"
    attese = {"2026-09-19-scrivere-con-ia.md": "ABCD", "2026-09-20-generativa-probabile.md": "ABC"}
    for nome, lettere in attese.items():
        if (idee / nome).exists():
            rr = richieste((idee / nome).read_text(encoding="utf-8"))
            assert "".join(r.sigla for r in rr) == lettere and all(len(r.testo) > 100 and "`" not in r.testo for r in rr)


def test_sigle_slug_e_comando():
    r = Richiesta("B", "errore", "Scrivi.")
    s = sigle(r, ["opus", "sonnet"], 5)
    assert [x[0] for x in s] == [f"B{k}" for k in range(1, 11)]
    assert [x[1] for x in s] == ["opus"] * 5 + ["sonnet"] * 5
    assert sigle(r, ["sonnet"], 2) == [("B1", "sonnet"), ("B2", "sonnet")]
    assert slug_e_data(Path("contenuti/idee/2026-09-19-scrivere-con-ia.md")) == ("scrivere-con-ia", "2026-09-19")
    assert slug_e_data(Path("senza-data.md")) == ("senza-data", None)
    c = comando(r, "opus")
    assert c[:3] == ["claude", "-p", "Scrivi."] and c[c.index("--model") + 1] == "opus"
    assert c[c.index("--tools") + 1] == "" and "--no-session-persistence" in c and c[-2:] == ["--output-format", "json"]
    assert c[c.index("--system-prompt") + 1] == "Sei un assistente che scrive testi su richiesta."


def test_estrai_result_da_oggetto_e_da_lista_di_eventi():
    assert estrai_result(json.dumps({"type": "result", "subtype": "success", "result": " Ecco la mail.\n"})) == "Ecco la mail."
    eventi = [{"type": "system", "subtype": "init"}, {"type": "assistant", "message": {}}, {"type": "result", "result": "Ecco."}]
    assert estrai_result(json.dumps(eventi)) == "Ecco."
    for rotto in ("non è json", json.dumps([{"type": "system"}]), json.dumps({"type": "result", "result": ""}),
                  json.dumps({"type": "result", "is_error": True, "result": "Credit balance is too low"})):
        with pytest.raises(ErroreUscite):
            estrai_result(rotto)


def test_anonimizza_parola_intera_maiuscole_e_conteggio():
    termini = termini_account("Ada Bianchi", "ada.bianchi@ateneo-vero.it", Config({"uscite": {"anonimizza": [["ateneo-vero.it", "ateneo.it"]]}}))
    assert termini[0] == ("ada.bianchi@ateneo-vero.it", "nome.cognome@email.it") and ("Bianchi", "Cognome") in termini
    testo, n = anonimizza("Mi chiamo ADA BIANCHI (ada.bianchi@ateneo-vero.it). Gentile signora Bianchi, la strada è bianchissima. "
                          "Scrivi a info@ateneo-vero.it. Adagio.", termini)
    assert testo == ("Mi chiamo Nome Cognome (nome.cognome@email.it). Gentile signora Cognome, la strada è bianchissima. "
                     "Scrivi a info@ateneo.it. Adagio.")
    assert n == 4
    assert anonimizza("Niente da togliere.", termini) == ("Niente da togliere.", 0)
    # un nome di tre parole non si spezza; senza sezione [uscite] e senza account non c'è niente da sostituire
    assert termini_account("Ada Maria Bianchi", "", Config({})) == [("Ada Maria Bianchi", "Nome Cognome")]
    assert termini_account("", "") == [] and anonimizza("Ada", [("", "x")]) == ("Ada", 0)


def test_segnalazioni_connettori_e_inferenze():
    assert segnalazioni("Ho provato ad aprire il tuo Google Drive, poi ti lascio la bozza in Gmail.") == ["Drive", "Gmail", "Google"]
    assert segnalazioni("Vedo che scrivi da un indirizzo universitario di Roma.") == ["Roma", "università"]
    assert segnalazioni("Spett.le Torrefazione di Pesaro, vi scrivo da Bologna.", richiesta="Annuncio: torrefazione (Bologna)") == []
    assert segnalazioni("Un romanzo, un drive-in.") == []


RR = [Richiesta("A", "base («migliora»)", "Migliora questa mail."), Richiesta("B", "la mossa", "Elenca i problemi.")]


def _uscite_finte(per_modello=1):
    return [Uscita(s, m, f"Testo {s}.") for r in RR for s, m in sigle(r, ["opus", "sonnet"], per_modello)]


def test_formato_del_file():
    md = componi("scrivere-con-ia", "2026-09-19", "2.1.278 (Claude Code)", RR, _uscite_finte(5), ["opus", "sonnet"], 5,
                 ["A1", "B7"], 3, {"A2": ["Drive"]})
    righe = md.splitlines()
    assert righe[0] == "# Uscite vere · scrivere-con-ia · 2026-09-19" and righe[1] == ""
    assert righe[2].startswith("Generate il 2026-09-19 dalla tappa T0b di `/pipeline`") and "`claude -p` (2.1.278 (Claude Code))" in righe[2]
    assert righe[3] == '`--model opus|sonnet --system-prompt "Sei un assistente che scrive testi su richiesta." --tools "" --no-session-persistence`.'
    assert "Sigle: 1-5 Opus, 6-10 Sonnet." in md and "2 uscite su 20, 3 sostituzioni: A1 B7" in md
    assert "«Nome Cognome»" in md and "«nome.cognome@email.it»" in md and "A schermo non vanno mai i dati veri." in md
    assert "non spegne i connettori" in md and "A2 (Drive)" in md
    assert "\n## A · base («migliora»)\n\n**Richiesta:**\n\n> Migliora questa mail.\n\n### A1 · Opus (opus)\n\nTesto A1.\n\n### A2 · Opus (opus)\n" in md
    assert "\n### A10 · Sonnet (sonnet)\n\nTesto A10.\n\n## B · la mossa\n\n**Richiesta:**\n\n> Elenca i problemi.\n\n### B1 · Opus (opus)\n" in md
    assert [r for r in righe if r.startswith("### ")][5] == "### A6 · Sonnet (sonnet)" and md.endswith("Testo B10.\n")
    pulito = componi("x", "2026-09-19", "v", RR, _uscite_finte(), ["opus", "sonnet"], 1, [], 0, {})
    assert "0 uscite su 4, 0 sostituzioni" in pulito and "nessuna uscita nomina" in pulito and "Sigle: 1-1 Opus, 2-2 Sonnet." in pulito


def test_scrivi_file_anonimizza_segnala_e_non_sovrascrive(tmp_path):
    fatte = _uscite_finte()
    fatte[0] = fatte[0]._replace(testo="Cordiali saluti,\nAda Bianchi\nada@esempio.it\n\nSe vuoi la salvo in Gmail.")
    dest = tmp_path / "uscite" / "x-2026-09-19.md"
    esito = scrivi_file(dest, "x", "2026-09-19", "v", RR, fatte, ["opus", "sonnet"], 1, termini_account("Ada Bianchi", "ada@esempio.it"))
    assert (esito["uscite"], esito["ritoccate"], esito["sostituzioni"], esito["segnalate"]) == (4, ["A1"], 2, {"A1": ["Gmail"]})
    md = dest.read_text(encoding="utf-8")
    assert "Ada" not in md and "esempio.it" not in md and "Nome Cognome\nnome.cognome@email.it" in md
    assert "1 uscite su 4, 2 sostituzioni: A1" in md and "A1 (Gmail)" in md
    with pytest.raises(ErroreUscite, match="esiste già"):
        scrivi_file(dest, "x", "2026-09-19", "v", RR, fatte, ["opus", "sonnet"], 1, [])
    scrivi_file(dest, "x", "2026-09-19", "v", RR, _uscite_finte(), ["opus", "sonnet"], 1, [], forza=True)
    assert "A1 (Gmail)" not in dest.read_text(encoding="utf-8")


def test_riga_uscite_aggiunta_sotto_lo_stato_e_non_duplicata():
    una = riga_uscite(IDEA, "contenuti/idee/uscite/x-2026-09-19.md")
    assert "**Stato:** idea\n**Uscite:** contenuti/idee/uscite/x-2026-09-19.md\n" in una
    due = riga_uscite(una, "contenuti/idee/uscite/x-2026-09-21.md")
    assert due.count("**Uscite:**") == 1 and "x-2026-09-21.md" in due and "x-2026-09-19.md" not in due
    assert due.replace("**Uscite:** contenuti/idee/uscite/x-2026-09-21.md\n", "") == IDEA      # il resto dell'idea non si tocca
    with pytest.raises(ErroreUscite, match="Stato"):
        riga_uscite("# Idea senza stato\n", "x.md")


def test_genera_in_parallelo_da_una_cartella_vuota(monkeypatch):
    viste, lucchetto = [], threading.Lock()

    def finta(cmd, cwd, timeout_s):
        with lucchetto:
            viste.append((cmd[2], cmd[cmd.index("--model") + 1], list(Path(cwd).iterdir()), timeout_s))
        return json.dumps([{"type": "system"}, {"type": "result", "result": f"{cmd[cmd.index('--model') + 1]}: {cmd[2]}"}])

    monkeypatch.setattr(uscite, "lancia", finta)
    passi = []
    fatte = genera(RR, ["opus", "sonnet"], 2, timeout_s=7, avanzamento=lambda s, k, n: passi.append((k, n)))
    assert [u.sigla for u in fatte] == ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]        # nell'ordine delle sigle, non d'arrivo
    assert fatte[0] == Uscita("A1", "opus", "opus: Migliora questa mail.") and fatte[6].testo == "sonnet: Elenca i problemi."
    assert len(viste) == 8 and all(vuota == [] and t == 7 for _, _, vuota, t in viste)
    assert sorted(passi) == [(k, 8) for k in range(1, 9)]


def test_un_fallimento_ferma_tutto_e_non_scrive_niente(monkeypatch, tmp_path):
    from tools.reel.__main__ import main
    idea = tmp_path / "2026-09-19-prova.md"
    idea.write_text(IDEA, encoding="utf-8")
    monkeypatch.setattr(uscite, "CARTELLA", tmp_path / "uscite")
    monkeypatch.setattr(uscite, "versione_claude", lambda: "0.0.0 (finto)")
    monkeypatch.setattr(uscite, "account_git", lambda: ("Ada Bianchi", "ada@esempio.it"))

    def rotta(cmd, cwd, timeout_s):
        if cmd[cmd.index("--model") + 1] == "sonnet":
            raise ErroreUscite("claude -p ha fallito (1): limite raggiunto")
        return json.dumps({"type": "result", "result": "Ecco."})

    monkeypatch.setattr(uscite, "lancia", rotta)
    assert main(["uscite", str(idea), "--per-modello", "1"]) == 1
    assert not (tmp_path / "uscite").exists() and idea.read_text(encoding="utf-8") == IDEA

    monkeypatch.setattr(uscite, "lancia", lambda cmd, cwd, timeout_s: json.dumps({"type": "result", "result": "Un saluto, Ada Bianchi"}))
    assert main(["uscite", str(idea), "--per-modello", "1"]) == 0
    (file,) = (tmp_path / "uscite").glob("prova-*.md")
    md = file.read_text(encoding="utf-8")
    assert "### C2 · Sonnet (sonnet)" in md and "Ada" not in md and "6 uscite su 6, 6 sostituzioni" in md
    assert f"**Stato:** idea\n**Uscite:** {file}\n" in idea.read_text(encoding="utf-8")
    assert main(["uscite", str(idea), "--per-modello", "1"]) == 1                              # il file di oggi c'è già
    assert main(["uscite", str(idea), "--per-modello", "1", "--forza"]) == 0
    assert idea.read_text(encoding="utf-8").count("**Uscite:**") == 1


def test_prova_a_secco_non_lancia_niente(monkeypatch, tmp_path, capsys):
    from tools.reel.__main__ import main
    idea = tmp_path / "2026-09-19-prova.md"
    idea.write_text(IDEA, encoding="utf-8")
    monkeypatch.setattr(uscite, "CARTELLA", tmp_path / "uscite")
    monkeypatch.setattr(uscite, "lancia", lambda *a, **k: pytest.fail("a secco non si lancia niente"))
    assert main(["uscite", str(idea), "--prova-a-secco", "--modelli", "opus"]) == 0
    out = capsys.readouterr().out
    assert "A · base («migliora»)  (A1…A5)" in out and out.count("$ claude -p") == 3 and "3 richieste × 1 modelli × 5 = 15 chiamate" in out
    assert not (tmp_path / "uscite").exists() and idea.read_text(encoding="utf-8") == IDEA
