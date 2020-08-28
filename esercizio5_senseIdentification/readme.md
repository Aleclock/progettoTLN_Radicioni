# **Sense identification**

<br/><br/>

# 0. INDIVIDUAZIONE DELLE COPPIE

>Le 50 coppie (sul totale di 500 coppie presenti nel file) sono da individuare sulla base del cognome, tramite la funzione definita nel notebook ``semeval_mapper.ipynb``.

<br/><br/>

# 1. ANNOTAZIONE DELLE COPPIE

> * La prima operazione consiste nell’annotare con punteggio di semantic similarity 50 coppie di termini.
> * Il criterio da utilizzare è il seguente (https://tinyurl.com/y6f8h2kd):
>
>   * `4: Very similar` -- The two words are synonyms (e.g., midday-noon).
>   * `3: Similar` --The two words share many of the important ideas of their meaning but include slightly different details.They refer to similar but not identical concepts (e.g., lion- zebra).
>   * `2: Slightly similar` -- The two words do not have a ver y similar meaning, but share a common topic/domain/function and ideas or concepts that are related (e.g., >house-window).
>   * `1: Dissimilar` -- The two items describe clearly dissimilar concepts, but may share some small details, a far relationship or a domain in common and might be >likely to be found together in a longer document on the same topic (e.g., software-keyboard).
>   * `0: Totally dissimilar and unrelated` -- The two items do not mean the same thing and are
>not on the same topic (e.g., pencil-frog).

La lista delle coppie ottenute è la seguente:

Term 1 | Term 2 | Value
:------------: | :------------: | :-------------:
terremoto|scossa |
patrimonio|azione |
ebreo|Gerusalemme |
nuvolosità|previsione |
dizionario|enciclopedia |
zecca|museo |
sedia|sgabello |
spagnolo|umidità |
lattina|bottiglia |
mosca|formica |
mito|satira |
centro della città|autobus |
coda|Boeing 747-200 |
opera d'arte|artista |
NATO|alleanza |
re|sovrano |
ritmo|cadenza |
Alexander Fleming|penicillina |
flauto|musica |
airone cenerino|lago |
viscosità|spruzzo |
hardware|case |
anello|fidanzamento |
latino|tedesco |
classe operaia|fabbrica |
Shakespeare|Dickens |
banconota|prete |
strumento|lavoro |
cinghiale nano|suidi |
suffragio|uscita |
stella|luminosità |
trota|chitarra |
dollaro|milionario |
cifra|numero |
burrasca|coperta |
Obama|Clinton |
personaggio secondario|film |
Juventus|Bayern Monaco |
cambiamento climatico|precipitazione |
IA|batteria |
capolavoro|Gioconda |
crimine|aggressione |
incoronazione|acqua |
vocalista|pentagramma |
spareggio|pallacanestro |
forze armate|difesa |
lago|nuvola |
monastero|doccia |
lingua madre|lingua |
porto|incarto |
