# Storico — broll

## 2026-09-22 · perso-nel-mezzo
- Scena 6 (telefono vecchio accanto al nuovo): due giri di query su Pexels senza una clip con i due oggetti insieme;
  risolta con due tagli (`--aggiungi`). Nella scena 4 molti candidati «grocery» erano dell'epoca covid, con le
  mascherine: scartati a vista.

## 2026-09-22 · gpu-comprare-o-affittare · clip senza volti, wow tecnologico
Sulle clip provvisorie del reel GPU (ragazzo sul divano, donna all'auto, uomo addormentato alla scrivania) Flavio:
«se non espressamente richiesto, meglio scegliere clip che non mostrano volti umani; preferire qualcosa che contiene
del tecnologico wow in funzione al resto». Regola in docs/regole-editoriali.md §3; negli agenti cosa cambia.

## 2026-09-22 · reel GPU · niente sala server su Pexels → nasce l'agente «immagini»
Per la scena 7 non esisteva una sala server senza persone: si è ripiegato su lucine sfocate. Flavio: «se non c'è un
candidato su pexel, la clip si potrebbe fare unendo 2-3 immagini fatte con meshy fatte passare con transizione», e
ha imposto **almeno una clip generata per reel**. Nasce l'agente `immagini` (T2c, in parallelo con broll e
animatore) e il comando `broll genera`; la regola sta in docs/regole-editoriali.md §3.

## 2026-09-23 · metà delle clip a Meshy
Flavio, rifacendo il reel GPU dal copione: le clip devono essere 50/50 fra fonte esterna (Pexels) e immagini generate
con Meshy e animate (zoom, pan, transizioni wow), e a Meshy vanno le scene i cui filmati convincono meno. Superata
«almeno una clip generata per reel» (2026-09-22). Regola in `docs/regole-editoriali.md` §3; per `broll` il passo 7 di
`scegli` (classifica di convinzione, metà più debole all'agente `immagini`). Libreria: `broll/broll/immagini.py` con
le mosse (`zoompan`) e `[transizioni] immagini` / `immagini_s`.

## 2026-09-23 · ia-e-lavoro · il piano che buttava le scelte dopo la registrazione
Dopo `reel parlato --applica` (il presentatore aveva corretto la VOCE in 8 scene registrando) `broll piano` ha rifatto
le scene 3, 5 e 8 come «da scegliere»: `eredita` voleva la VOCE identica, e con essa sparivano anche le immagini Meshy
pagate. Ripristinato piano.json dal commit; corretto `piano.eredita`: una scena già `[broll]` eredita anche con la VOCE
cambiata, con una nota «riguarda il filmato sul testo nuovo». Nessuna regola nuova per l'agente: era la libreria.
