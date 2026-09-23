<!--
Il prompt del copione (`uv run reel copione <idea>`, tools/reel/copione.py): lo ricevono così com'è i modelli della
catena di `config.toml [copione] modelli`. È il testo della prova alla cieca del 2026-09-23 (gpt-5.4 > deepseek >
gemini > Claude), reso generale. I segnaposto {{…}} li riempie il comando; questo commento non parte.
Si cambia qui, non nel codice: ogni riga costa punti Poe a ogni corsa, quindi niente regole che il modello non usa.
-->
Prima di scrivere, leggi queste trascrizioni di reel italiani veri (trascritte in automatico, possono avere errori): prendi il passo, il ritmo e il modo di parlare, non le frasi né i fatti.

{{trascrizioni}}

--- fine trascrizioni ---

Scrivi il parlato (quello che il presentatore dice a camera) di un reel Instagram italiano di circa {{secondi}} secondi, {{scene}} scene, al massimo {{parole}} parole in tutto. Il presentatore parla a camera in modo naturale, come a un amico, stile social italiano. Il reel si guarda anche muto con le caption, ma la voce deve suonare parlata, non scritta: niente frasi da titolo, niente aforismi in fila, niente simmetrie tipo «X, sì. Y, no.», verbo in ogni frase, frasi di lunghezza diversa, connettivi parlati. Un solo effetto a battuta, alla fine.

Tema: {{tema}}
Messaggio: {{messaggio}}

Contenuto per scena (i fatti sono questi e solo questi; il modo di dirli è tuo). Fra parentesi cosa si vede mentre parla: «apertura» e «chiusura» sono lui a tutto schermo; sotto un «filmato» la voce resta generica, senza numeri né termini tecnici; sotto un'«animazione» si spiega il meccanismo e stanno i numeri.
{{tappe}}

Limiti: la scena di apertura al massimo {{hook_max}} parole, quella di chiusura al massimo {{chiusura_max}}, nessuna scena oltre {{scena_max}}.

Vincoli: numeri scritti in lettere come si dicono (centodieci, millecinquecento), niente sigle da sciogliere, niente elenchi, niente «ciao ragazzi», niente CTA «seguimi». Nessun fatto oltre a quelli sopra.
{{nota}}
Formato di uscita, solo questo:
## Scena 1
<parlato>
## Scena 2
<parlato>
... fino a Scena {{scene}}.
