from pathlib import Path

import pytest

from tools.reel import copione as cp
from tools.reel.copione import (ErroreChiamata, ErroreCopione, catena, componi_file, componi_prompt,
                                esamina, leggi_copione, leggi_idea, leggi_uscita, riga_copione, scegli_trascrizioni)

IDEA = """# Comprare una scheda conviene solo se la usi

**Data:** 2026-09-22
**Stato:** idea

## Messaggio centrale
Una scheda comprata costa meno a ogni ora
che la usi.

## Tappe del parlato
<!-- un commento -->
1. (apertura) Una domanda: quante ore la userai?
2. (filmato: uno sul divano) Le schede costano
   più di prima.
3. (animazione) Mezzo euro l'ora a noleggio.
4. (filmato: un'auto a noleggio) La macchina tua costa meno più la usi.
5. (chiusura) Conta le ore.

## Note per il reel
1. questo non è una tappa
"""


def _uscita(scene: dict[int, str]) -> str:
    return "Ecco il testo.\n\n" + "\n".join(f"## Scena {n}\n{t}\n" for n, t in scene.items())


BUONO = {1: "Stai per comprare una scheda video? Ma quante ore la userai davvero?",
         2: "Perché se apri gli annunci vedi che costano molto più di quanto ti ricordavi.",
         3: "A noleggio paghi circa mezzo euro l'ora, sempre, che tu la usi poco o tanto.",
         4: "Pensa alla macchina, che se è tua costa meno a viaggio più la usi.",
         5: "Quindi prima di comprarla conta le ore, che è lì che si decide."}


def test_idea_tappe_messaggio_e_tema():
    idea = leggi_idea(IDEA)
    assert idea.tema == "Comprare una scheda conviene solo se la usi"
    assert idea.messaggio == "Una scheda comprata costa meno a ogni ora che la usi."
    assert [t.n for t in idea.tappe] == [1, 2, 3, 4, 5]
    assert idea.tappe[1].testo == "(filmato: uno sul divano) Le schede costano più di prima."


def test_idea_senza_tappe_o_numerata_male():
    with pytest.raises(ErroreCopione, match="Tappe del parlato"):
        leggi_idea(IDEA.replace("## Tappe del parlato", "## Altro"))
    with pytest.raises(ErroreCopione, match="numerate male"):
        leggi_idea(IDEA.replace("3. (animazione)", "7. (animazione)"))
    with pytest.raises(ErroreCopione, match="tappe"):
        leggi_idea(IDEA.replace("4. (filmato", "x").replace("5. (chiusura)", "x"))


def test_riga_copione_e_stato():
    t = riga_copione(IDEA, "contenuti/copioni/x.md")
    assert "**Stato:** copione\n**Copione:** contenuti/copioni/x.md" in t
    t2 = riga_copione(t.replace("**Stato:** copione", "**Stato:** sceneggiata"), "contenuti/copioni/y.md")
    assert t2.count("**Copione:**") == 1 and "**Stato:** sceneggiata" in t2 and "y.md" in t2


def test_trascrizioni_una_per_account_e_stabili():
    voci = [{"id": f"r{i:02d}", "account": f"a{i % 4}", "durata_s": 60 + i * 3, "parole_al_s": 3.0} for i in range(20)]
    voci.append({"id": "lento", "account": "z", "durata_s": 85, "parole_al_s": 1.0})
    s = scegli_trascrizioni(voci, "slug", 6, 85)
    assert len(s) == 6 and "lento" not in [v["id"] for v in s]
    assert len({v["account"] for v in s[:4]}) == 4
    assert s == scegli_trascrizioni(list(reversed(voci)), "slug", 6, 85)


def test_prompt_riempie_i_segnaposto():
    idea = leggi_idea(IDEA)
    tpl = cp.TEMPLATE.read_text(encoding="utf-8")
    p = componi_prompt(tpl, idea, [("r01", "ciao a tutti\n")], 200, nota="più corto")
    assert "{{" not in p and "<!--" not in p
    assert "--- trascrizione r01 ---\nciao a tutti" in p
    assert "5 scene, al massimo 200 parole" in p and "fino a Scena 5." in p
    assert "fra 160 e 200 parole in tutto, cioè circa 40 per scena" in p and "tieni i due che contano di più" in p
    assert "2. (filmato: uno sul divano) Le schede costano più di prima." in p
    assert "Richiesta del presentatore per questa versione: più corto" in p
    assert "Richiesta del presentatore" not in componi_prompt(tpl, idea, [], 200)


def test_leggi_uscita_toglie_saluti_e_formattazione():
    s = leggi_uscita("Certo!\n\n### Scena 1\n<parlato>\n**Ciao** a te.\n</parlato>\n## Scena 2 — filmato\n\"Due\n righe.\"\n")
    assert s == {1: "Ciao a te.", 2: "Due righe."}


def test_esame():
    assert esamina(BUONO, 5, 235) == ([], [], [], [])
    e = esamina({**BUONO, 3: "Costa 0,53 euro l'ora " + "e poi " * 40}, 5, 60)
    assert not e.errori
    assert any("cifre (0,53)" in c for c in e.correggibili) and any("in tutto" in a for a in e.avvisi)
    assert any("scena 3 ha" in a for a in e.avvisi)          # dal 2026-09-23 solo l'apertura si corregge
    assert any("apertura ha" in c for c in esamina({**BUONO, 1: "parola " * 30}, 5, 235).correggibili)
    assert esamina({1: "x", 2: "y"}, 5, 235).errori
    lunga_chiusura = esamina({**BUONO, 5: "parola " * 30}, 5, 235)
    assert any("chiusura ha 30" in a for a in lunga_chiusura.avvisi) and not lunga_chiusura.correggibili
    stile = esamina({**BUONO, 2: "Fluente, sì. Originale, no. Il testo non lo cerca: lo scrive lei."}, 5, 235)
    assert stile.avvisi and not stile.correggibili


def test_catena_primo_buono():
    chiamati = []
    def chiama(m, p):
        chiamati.append(m)
        return _uscita(BUONO)
    e = catena("P", ["gpt", "deep", "claude"], 5, 235, chiama)
    assert e.modello == "gpt" and chiamati == ["gpt"] and e.tentativi == ["gpt: ok"]


def test_catena_402_e_saldo_basso_scendono():
    chiamati = []
    def chiama(m, p):
        chiamati.append(m)
        if m == "gpt":
            raise ErroreChiamata("HTTP 402")
        return _uscita(BUONO)
    salta = lambda m, p: "saldo 100 punti" if m == "deep" else None
    e = catena("P", ["gpt", "deep", "gemini"], 5, 235, chiama, salta)
    assert e.modello == "gemini" and chiamati == ["gpt", "gemini"]
    assert e.tentativi[0].startswith("gpt: fallito") and e.tentativi[1] == "deep: saltato (saldo 100 punti)"


def test_catena_corregge_una_volta_lo_stesso_modello():
    lungo = {**BUONO, 3: BUONO[3] + " E costa 1500 euro."}
    risposte = iter([_uscita(lungo), _uscita(BUONO)])
    prompt = []
    def chiama(m, p):
        prompt.append(p)
        return next(risposte)
    e = catena("P", ["gpt", "deep"], 5, 235, chiama)
    assert e.modello == "gpt" and len(prompt) == 2
    assert "numeri in cifre (1500)" in prompt[1] and "## Scena 3" in prompt[1]
    assert e.tentativi[0].startswith("gpt: corretto")


def test_catena_tiene_il_lungo_dopo_la_correzione_ma_non_oltre_il_tetto():
    lungo = {**BUONO, 5: "parola " * 30}
    e = catena("P", ["gpt", "deep"], 5, 235, lambda m, p: _uscita(lungo), tetto=300)
    assert e.modello == "gpt" and any("chiusura ha 30" in a for a in e.esame.avvisi) and not e.esame.correggibili
    enorme = {**BUONO, 3: "parola " * 45, 2: "parola " * 45, 4: "parola " * 45}
    e = catena("P", ["gpt", "deep"], 5, 235, lambda m, p: _uscita(enorme if m == "gpt" else BUONO), tetto=120)
    assert e.modello == "deep" and "oltre 120" in e.tentativi[0]


def test_catena_scarta_se_la_correzione_non_basta_e_poi_fallisce_tutto():
    lungo = {**BUONO, 3: "costa 1500 euro"}
    e = catena("P", ["gpt", "deep"], 5, 235, lambda m, p: _uscita(lungo if m == "gpt" else BUONO))
    assert e.modello == "deep" and e.tentativi[0].startswith("gpt: scartato")
    with pytest.raises(ErroreCopione, match="nessun modello"):
        catena("P", ["gpt"], 5, 235, lambda m, p: "niente scene")


def test_file_copione_si_rilegge():
    idea = leggi_idea(IDEA)
    esito = catena("P", ["gpt"], 5, 235, lambda m, p: _uscita(BUONO))
    testo = componi_file("contenuti/idee/x.md", idea, esito, "2026-09-23", 812, nota="più corto")
    assert testo.startswith("---\nidea: contenuti/idee/x.md\nmodello: gpt\n")
    assert "punti_poe: 812" in testo and "nota: più corto" in testo
    assert leggi_copione(testo) == BUONO


def test_chiave_poe_da_env(tmp_path, monkeypatch):
    monkeypatch.delenv("POE_API_KEY", raising=False)
    monkeypatch.setattr(cp, "RADICE", tmp_path)
    assert cp.chiave_poe() is None
    (tmp_path / ".env").write_text("ALTRO=1\nexport POE_API_KEY=\"abc\"\n")
    assert cp.chiave_poe() == "abc"
    monkeypatch.setenv("POE_API_KEY", "xyz")
    assert cp.chiave_poe() == "xyz"


def test_stima_punti():
    poe = cp.Poe.__new__(cp.Poe)
    poe.token_uscita, poe.punti_minimi = 1000, 1500
    poe._prezzi = {"a": {"prompt": "0.000001", "completion": "0.00001"}, "b": {"request": "0.015"}}
    assert poe.stima_punti("a", "x" * 3200) == int((0.001 + 0.01) / cp.USD_PER_PUNTO) + 1
    assert poe.stima_punti("b", "x") == int(0.015 / cp.USD_PER_PUNTO) + 1
    assert poe.stima_punti("ignoto", "x") is None


def test_idea_gpu_del_repo():
    p = Path(__file__).resolve().parents[1] / "contenuti" / "idee" / "2026-09-22-gpu-comprare-o-affittare.md"
    if p.exists() and "## Tappe del parlato" in p.read_text(encoding="utf-8"):
        assert len(leggi_idea(p.read_text(encoding="utf-8")).tappe) == 9


def test_saldo_prudente_non_si_fida_del_saldo_in_ritardo():
    poe = cp.Poe.__new__(cp.Poe)
    poe.token_uscita, poe.punti_minimi = 1000, 1500
    poe._prezzi = {"a": {"request": "0.06"}}          # 2.001 punti a chiamata
    poe._primo_saldo, poe._impegnati = None, 0
    poe.saldo = lambda: 4000                          # Poe non ha ancora scalato niente
    assert poe.salta("a", "x") is None
    poe._impegnati += poe.stima_punti("a", "x")      # come fa `chiama`
    assert poe.saldo_prudente() == 4000 - 2001
    assert "stima" in poe.salta("a", "x")             # 1.999 < 2.001: la seconda non parte


def test_ogni_risposta_si_archivia_anche_scartata():
    salvate = []
    cifre = {**BUONO, 3: "costa 1500 euro"}
    risposte = {"gpt": [_uscita(cifre), _uscita(cifre)], "deep": [_uscita(BUONO)]}
    e = catena("P", ["gpt", "deep"], 5, 235, lambda m, p: risposte[m].pop(0),
               archivia=lambda m, fase, t: salvate.append((m, fase)))
    assert e.modello == "deep"
    assert salvate == [("gpt", "prima"), ("gpt", "correzione"), ("deep", "prima")]


def test_taratura_delle_parole_per_modello():
    assert cp.parole_per("gpt-5.4", 235, {"gpt-5.4": 0.8}) == 188
    assert cp.parole_per("claude", 235, {"gpt-5.4": 0.8}) == 235
    assert cp.parole_per("gpt-5.4", 235, None) == 235


def test_la_taratura_scala_anche_i_limiti_per_scena():
    idea = leggi_idea(IDEA)
    p = componi_prompt(cp.TEMPLATE.read_text(encoding="utf-8"), idea, [], 188, fattore=0.8)
    assert "l'apertura al massimo 20 parole" in p and "niente due punti come snodo" in p
