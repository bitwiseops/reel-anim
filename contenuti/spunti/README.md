# Spunti

Il punto di partenza di un reel: un link a un articolo, due-tre righe del presentatore o un tema. Un file per spunto,
`AAAA-MM-GG-<slug>.md`, con questo frontmatter; nel corpo le righe, il tema o una nota sul link:

```
---
fonte: url            # url | testo | tema
url: https://…        # solo con fonte: url
data: 2026-09-15
stato: spunto         # l'ideatore lo porta a «ideato» e aggiunge «idea: contenuti/idee/…»
---
```

Poi `/pipeline contenuti/spunti/<file>` (a fermate) o `/pipeline contenuti/spunti/<file> --tutto` (fino all'anteprima
da registrare).
