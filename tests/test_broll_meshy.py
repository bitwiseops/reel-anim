"""Meshy con la rete finta: nessuna immagine vera viene generata da questi test."""
from __future__ import annotations

import json

import pytest
import requests

from tools.broll.fornitori import FornitoreNonConfigurato, RichiestaFallita
from tools.broll.fornitori import meshy


class _Risposta:
    def __init__(self, stato=200, dati=None, testo=""):
        self.status_code = stato
        self._dati = dati or {}
        self.text = testo or json.dumps(self._dati)

    @property
    def ok(self):
        return 200 <= self.status_code < 300

    def json(self):
        return self._dati


# --- chiavi e failover ----------------------------------------------------------------------------

def test_le_chiavi_non_finiscono_mai_nei_messaggi(monkeypatch):
    monkeypatch.setattr(meshy, "chiavi", lambda: [])
    with pytest.raises(FornitoreNonConfigurato) as e:
        meshy.con_failover(lambda k: "mai")
    assert "MESHY_API_KEY" in str(e.value) and "segreta" not in str(e.value)


def test_failover_sulla_riserva_quando_i_crediti_finiscono():
    provate: list[str] = []

    def apri(k: str) -> str:
        provate.append(k)
        if k == "prima":
            raise meshy.CreditiEsauriti("402")
        return "task-2"

    task, usata = meshy.con_failover(apri, elenco=["prima", "riserva"])
    assert (task, usata) == ("task-2", "riserva")
    assert provate == ["prima", "riserva"]


def test_senza_crediti_su_nessuna_chiave_si_ferma():
    def apri(k: str) -> str:
        raise meshy.CreditiEsauriti("402")

    with pytest.raises(meshy.CreditiEsauriti):
        meshy.con_failover(apri, elenco=["a", "b"])


def test_402_e_i_corpi_che_parlano_di_crediti_sono_failover():
    with pytest.raises(meshy.CreditiEsauriti):
        meshy._solleva(_Risposta(402, testo="nope"), "text-to-image")
    with pytest.raises(meshy.CreditiEsauriti):
        meshy._solleva(_Risposta(400, testo="insufficient balance"), "text-to-image")
    with pytest.raises(FornitoreNonConfigurato):
        meshy._solleva(_Risposta(401, testo="bad key"), "text-to-image")
    with pytest.raises(RichiestaFallita):
        meshy._solleva(_Risposta(500, testo="boom"), "text-to-image")


# --- POST, polling, download ----------------------------------------------------------------------

def test_avvia_manda_prompt_modello_e_formato(monkeypatch):
    visti = {}

    def post(url, json=None, headers=None, timeout=None):
        visti.update(url=url, corpo=json, headers=headers)
        return _Risposta(200, {"result": "t-1"})

    monkeypatch.setattr(meshy.requests, "post", post)
    assert meshy.avvia("un gatto", "segreta") == "t-1"
    assert visti["url"].endswith("/openapi/v1/text-to-image")
    assert visti["corpo"] == {"prompt": "un gatto", "ai_model": meshy.MODELLO, "aspect_ratio": "9:16"}
    assert visti["headers"]["Authorization"] == "Bearer segreta"


def test_attendi_polla_fino_a_succeeded(monkeypatch):
    risposte = [_Risposta(200, {"status": "PENDING", "progress": 0}),
                _Risposta(200, {"status": "IN_PROGRESS", "progress": 50}),
                _Risposta(200, {"status": "SUCCEEDED", "progress": 100,
                                "image_urls": ["https://x/img.png"]})]
    monkeypatch.setattr(meshy.requests, "get", lambda *a, **k: risposte.pop(0))
    monkeypatch.setattr(meshy.time, "sleep", lambda _: None)
    task = meshy.attendi("t-1", "segreta", intervallo_s=0, avanzamento=lambda q, s: None)
    assert meshy.url_immagine(task) == "https://x/img.png"
    assert risposte == []


def test_attendi_si_ferma_su_failed(monkeypatch):
    monkeypatch.setattr(meshy.requests, "get",
                        lambda *a, **k: _Risposta(200, {"status": "FAILED", "task_error": "brutto"}))
    monkeypatch.setattr(meshy.time, "sleep", lambda _: None)
    with pytest.raises(meshy.TaskFallito):
        meshy.attendi("t-1", "segreta", intervallo_s=0, avanzamento=lambda q, s: None)


def test_un_task_riuscito_senza_immagine_e_un_errore():
    with pytest.raises(RichiestaFallita, match="senza immagine"):
        meshy.url_immagine({"status": "SUCCEEDED", "image_urls": []})


def test_la_rete_giu_diventa_richiesta_fallita(monkeypatch):
    def post(*a, **k):
        raise requests.RequestException("giù")

    monkeypatch.setattr(meshy.requests, "post", post)
    with pytest.raises(RichiestaFallita, match="non raggiungibile"):
        meshy.avvia("x", "segreta")


# --- cache ----------------------------------------------------------------------------------------

def _finta_rete(monkeypatch, conteggio: dict):
    def post(url, json=None, headers=None, timeout=None):
        conteggio["post"] = conteggio.get("post", 0) + 1
        return _Risposta(200, {"result": f"t-{conteggio['post']}"})

    def get(url, headers=None, timeout=None, stream=False):
        if stream:
            return _Scarico()
        return _Risposta(200, {"status": "SUCCEEDED", "progress": 100,
                               "image_urls": ["https://x/img.png"]})

    monkeypatch.setattr(meshy.requests, "post", post)
    monkeypatch.setattr(meshy.requests, "get", get)
    monkeypatch.setattr(meshy, "chiavi", lambda: ["segreta"])
    monkeypatch.setattr(meshy.time, "sleep", lambda _: None)


class _Scarico:
    status_code = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size=0):
        yield b"\x89PNG finto"


def test_il_nome_in_cache_e_il_prompt_piu_indice(tmp_path):
    a = meshy.file_cache("un gatto", 1, tmp_path)
    b = meshy.file_cache("un gatto", 2, tmp_path)
    c = meshy.file_cache("un cane", 1, tmp_path)
    assert a.name.startswith("meshy-") and a.name.endswith("-1.png")
    assert a != b and a != c
    assert meshy.file_cache(" un gatto  ", 1, tmp_path) == a     # gli spazi ai bordi non contano


def test_la_cache_evita_la_seconda_chiamata(tmp_path, monkeypatch):
    conteggio: dict = {}
    _finta_rete(monkeypatch, conteggio)

    f1, s1 = meshy.genera("un gatto nero", 1, cache=tmp_path)
    assert f1.exists() and s1["da_cache"] is False and conteggio["post"] == 1
    assert s1["prompt"] == "un gatto nero" and s1["modello"] == meshy.MODELLO

    f2, s2 = meshy.genera("un gatto nero", 1, cache=tmp_path)
    assert f2 == f1 and s2["da_cache"] is True
    assert conteggio["post"] == 1                               # la rete non è stata toccata

    meshy.genera("un gatto nero", 2, cache=tmp_path)            # altro indice, altra immagine
    assert conteggio["post"] == 2

    meshy.genera("un gatto nero", 1, cache=tmp_path, forza=True)
    assert conteggio["post"] == 3                               # --forza ripaga, e lo dice


def test_la_scheda_in_cache_conserva_task_e_data(tmp_path, monkeypatch):
    _finta_rete(monkeypatch, {})
    _, prima = meshy.genera("un cane", 1, cache=tmp_path)
    _, dopo = meshy.genera("un cane", 1, cache=tmp_path)
    assert dopo["task"] == prima["task"] and dopo["quando"] == prima["quando"]
    assert dopo["generata"] is True and dopo["licenza"] == meshy.LICENZA
