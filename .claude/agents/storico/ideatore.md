# Storico delle lezioni · ideatore

Copia integrale della sezione «Lezioni dalle sessioni» di `.claude/agents/ideatore.md` com'era il 2026-09-21, prima del
riordino in «Regole in vigore». **Gli agenti non caricano questo file**: è la cronaca (chi ha detto cosa, su quale
reel, cosa è stato superato e da cosa). Le lezioni nuove si aggiungono in fondo, con la data, quando serve ricordare
il *perché* di una regola; la regola stessa vive nell'agente.

## Dove è finita ogni lezione (riordino del 2026-09-21)
| Lezione | Oggi |
|---|---|
| 09-15 · conti grezzi senza plurali | in vigore · «Fonti e numeri» |
| 09-15 · in `--tutto` consiglia un'opzione per domanda | in vigore · «In `--tutto`» |
| 09-15 · set di testi con richieste identiche alle carte | in vigore · «Testi del modello» |
| 09-19 · hook = frase + clip dietro, niente titolo a schermo | **superata la clip dietro** (09-21, estremi a volto pieno, regole editoriali §4). Resta in vigore · «Percorso e registri»: primi 5-10 s, hook = problema o domanda e non la tesi, titolo di copertina = tesi, test dell'immagine filmabile (ora sulle tappe a filmato) |
| 09-19 · ogni reel è a sé stante | in vigore · «Situazione e nomi» + regole editoriali §6 |
| 09-20 · la mossa del reel è della fonte? | in vigore, **corretta** · «Fonti e numeri»: il credito va in caption, il reel non attribuisce (superato «il reel la attribuisce», regole editoriali §5) |
| 09-20 · omonimia anche nel settore dei personaggi | in vigore · «Situazione e nomi» |
| 09-20 · query dei filmati in inglese | in vigore, **corretta** · «Percorso e registri»: per le tappe a filmato, non più per l'hook |
| 09-20 · leggi tutto, traccia solo le fonti ufficiali (anche con `fonte: url`) | in vigore · «Fonti e numeri» + regole editoriali §5 |
| 09-21 · i due registri stanno a metà | in vigore · «Percorso e registri» + regole editoriali §3 |
| 09-21 · apertura e chiusura a tutto schermo | in vigore · «Percorso e registri» + regole editoriali §4 |

## Lezioni dalle sessioni
- **2026-09-15, prima corsa** (spunto «testo», rifacimento del reel d'esempio `generativa-probabile`):
  - I conti grezzi del file delle uscite non contano i plurali («sveglie»): ogni numero che passi al reel va
    ricontato sulle uscite, con la sigla di ciascuna. Il revisore li ha ritrovati tutti così.
  - Chiudere con DONE_WITH_CONCERNS e domande al presentatore va bene, ma in `--tutto` nessuno risponde prima della
    fine: scrivi per ogni domanda quale opzione consigli e perché, così il coordinatore sceglie la tua.
  - Il set di testi del modello con le richieste identiche alle carte a schermo (A2/C2/D2) ha evitato il «richieste
    quasi uguali» del primo reel: quando si riusano uscite vere, cercalo per primo.
- **[SUPERATA il 2026-09-21: l'apertura è il presentatore a tutto schermo, vedi la regola in fondo]** **2026-09-19, nota del presentatore sull'apertura**: i primi 5-10 secondi
  devono catturare l'attenzione. L'hook porta **un problema o una domanda** di chi guarda, non la tesi; e dietro, in
  quel momento, si vede **una clip che richiama quel problema** (materiale filmato, non una carta Manim). Nelle
  «Note per il reel» l'hook candidato va scritto in coppia: la frase **e** l'immagine che la accompagna («chi apre
  la posta il lunedì mattina con la casella piena»), concreta abbastanza da poterla cercare su un banco di filmati.
  Se per il problema non ti viene in mente un'immagine filmabile, il problema è ancora troppo astratto.
  Decisione del presentatore sullo stesso punto: **a schermo nell'apertura non c'è il titolo**, c'è lui nel riquadro
  sopra la clip; il titolo che proponi serve alla copertina (la griglia del profilo), quindi può restare la tesi.
- **2026-09-19, regola del presentatore: «ogni reel è a sé stante, non c'è una storia temporale continua»** (detta
  alla fermata 1 di `scrivere-con-ia`: l'idea riusava «Acme Arredi» e la vicenda di `generativa-probabile`, «il posto
  l'hai avuto», come continuità). Chi guarda un reel non ha visto gli altri. La situazione di ogni idea è nuova:
  azienda, persone e vicenda inventate da capo, nessun personaggio che prosegue, nessun «seguito di», nessun
  richiamo a voce o a schermo a un reel precedente. Gli altri reel si leggono solo per **non ripetersi** (angoli,
  schemi già spesi, claim già verificati): questo resta nelle note interne dell'idea, mai nella Situazione, nella
  Struttura narrativa o nelle richieste da generare. Un concetto già spiegato altrove si ridice in una frase, come
  se fosse la prima volta.

### 2026-09-20 · corse `scrivere-con-ia` e `generativa-probabile`
- **La mossa del reel è della fonte?** Con `fonte: url`, prima di scrivere «la nostra mossa è più mite / diversa da
  quella dell'autore», rileggi il metodo che l'autore descrive: in `scrivere-con-ia` la mossa («chiedi i problemi,
  riscrivi tu») era parola per parola il metodo di Ptacek, e il revisore ha dato ❌ alla riga che la presentava come
  nostra. Se la mossa è sua, l'idea lo dice e il reel la attribuisce.
- **Omonimia: cerca anche nel settore dei personaggi.** «Quattroassi Arredi» non aveva omonimi fra i negozi di arredi,
  ma esisteva una Quattroassi S.r.l. che gestisce un bar, e la cliente del reel apriva un bar. Cerca il nome da solo,
  non solo «nome + settore dell'azienda». Se il nome sta dentro le richieste da generare, l'omonimia va chiusa prima
  di T0b: dopo, cambiarlo vuol dire rigenerare tutte le uscite.
- **Le query dei filmati in inglese.** Le tre query per Pexels che scrivi nell'hook servono davvero: `broll piano` le
  ricava dalle parole italiane del brief e Pexels le capisce male («piedi» → otto filmati di piedi nudi). Scrivile
  sempre, in inglese, anche per le scene d'attenzione candidate.

### 2026-09-20 · REGOLA DEL PRESENTATORE: leggi tutto, traccia solo le fonti ufficiali
Nota di Flavio sullo spunto `ia-e-lavoro`. Quando uno spunto chiede dati o contesto (`fonte: testo` o `tema`):
- **Cerca e leggi sul web anche gli articoli che ne parlano** (giornali, blog, newsletter): servono a capire quali
  numeri girano, quali esempi e quali obiezioni. Questo materiale informa l'idea e **non si cataloga**: niente elenco di
  URL, date di consultazione e citazioni per ogni articolo letto.
- **In `## Fonte` e nei «Claim per il revisore» entrano solo fonti ufficiali**: istituzioni e organismi (WEF, FMI, OCSE,
  ILO, Commissione europea, Eurostat, Eurobarometro, Banca d'Italia, Istat, INAPP), studi accademici pubblicati,
  istituti di ricerca riconosciuti (Pew, Gallup, McKinsey Global Institute, Goldman Sachs Research). Per queste resta il
  rigore: chi, anno, link, **cosa misura alla lettera**.
- **Niente opinioni di gente a caso**: la tesi di un commentatore o di un post non entra nel reel né come claim né come
  autorità. Se un articolo riporta un numero interessante, risali alla fonte ufficiale: se la trovi citi quella, se non
  la trovi il numero non entra.
- **Vale anche con `fonte: url`** (precisazione del presentatore, stesso giorno): se il link è il post di una persona
  qualunque (un blogger, un programmatore, un commentatore: il post di Ptacek per `scrivere-con-ia`), è **uno spunto di
  riflessione**, non un'autorità. Lo leggi, ne prendi le idee, ma **nel reel non si cita**: niente nome a voce o a
  schermo, niente «secondo X», niente sue frasi come punch. Il credito va **nella caption** («l'idea viene da un post
  di …», con il link), e l'idea lo scrive nelle note per la caption. Onestà: il reel non dice «me lo sono inventato
  io» né presenta come dimostrata una sua opinione; la mossa si presenta per quello che è, senza paternità. A voce o a
  schermo si citano solo fonti ufficiali.
- Nel rapporto: i due-tre numeri scelti con la fonte ufficiale, e in due righe cosa hai capito dal resto della lettura.

### 2026-09-21 · REGOLA DEL PRESENTATORE: i due registri stanno a metà
Nota di Flavio davanti ai due reel del regime muto: erano 2 scene a filmato su 7, cioè cinque scene animate di fila.
Da qui in poi **circa metà delle scene di un reel va a filmato** (± una), e la divisione riguarda anche il parlato:
sulle clip la voce dice le cose **generiche** (il problema, l'esperienza riconosciuta, la conseguenza, il passaggio),
nelle animazioni va la **spiegazione complessa** (meccanismo, quantità, confronti).

Cosa cambia per te, nelle «Note per il reel»:
- il **Percorso** che proponi deve già alternare i due registri e arrivare a metà per metà: segna per ogni tappa se è
  **animata** (cosa si disegna) o **a filmato** (cosa si vede), e non metterne mai due a filmato di fila;
- una tappa a filmato va scritta **senza numeri e senza termini tecnici**: se il suo contenuto ha una cifra, quella
  cifra appartiene alla tappa animata accanto. È il segnale con cui `broll piano` decide, e una sola frase tecnica in
  mezzo fa restare la scena a Manim;
- per **ogni** tappa a filmato (non solo per l'hook) scrivi l'immagine concreta e **2-3 query in inglese**;
- se per stare a metà servono più tappe, proponile: le scene a filmato sono corte (4-7 s) e non allungano il reel.
Se per una tappa generica non riesci a immaginare un'immagine filmabile, quella tappa è ancora troppo astratta:
riscrivila come esperienza concreta, non come concetto.

### 2026-09-21 · REGOLA DEL PRESENTATORE: apertura e chiusura sono lui, a tutto schermo
L'hook non ha più una clip dietro: **è il presentatore a tutta tela** che pone il problema guardando in camera, e la
chiusura è lui che dice la conclusione, con le sole caption (niente messaggio a schermo: il MESSAGGIO candidato va
nella caption del post). Quindi nelle «Note per il reel»:
- l'**hook candidato** è **la frase** da dire in faccia a chi guarda — un problema o una domanda sua, ≤ 20 parole —
  e non più la coppia frase + immagine. Niente query per l'hook;
- le immagini filmabili e le query in inglese servono alle **tappe a filmato in mezzo** (regola dei registri a metà,
  qui sopra), che si contano **senza** apertura e chiusura;
- il TITOLO di copertina resta la tesi.

## 2026-09-22 · perso-nel-mezzo
- Il criterio proposto nell'idea («chiedile la frase esatta») è finito in un ❌ del revisore alla sceneggiatura: un
  modello può restituire una frase parafrasata o inventata. Serve il gesto di controllo di chi guarda.

## 2026-09-23 · le tappe del parlato
Con il copione scritto da un modello esterno prima della sceneggiatura (vedi storico dello sceneggiatore, stessa
data) serve un brief per scena: l'idea porta `## Tappe del parlato`, nel formato del brief della prova alla cieca
(`contenuti/prove-parlato/gpu-comprare-o-affittare/brief.md`). Prende il posto del **Percorso** nelle Note per il reel.
