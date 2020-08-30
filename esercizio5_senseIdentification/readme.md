# **Sense identification**

<br/><br/>

# 0. INDIVIDUAZIONE DELLE COPPIE

>Le 50 coppie (sul totale di 500 coppie presenti nel file) sono da individuare sulla base del cognome, tramite la funzione definita nel notebook ``semeval_mapper.ipynb``. Le coppie individuato dal cognome Clocchiatti sono

~~~~plain
Clocchiatti    :        coppie nell'intervallo 201-250
~~~~

<br/><br/>

# 1.1 ANNOTAZIONE DELLE COPPIE

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

<br/><br/>

# 1.2 VALUTAZIONE ANNOTAZIONE

>1. La valutazione dei punteggi annotati dovrà essere condotta in rapporto alla similarità ottenuta utilizzando i vettori NASARI (versione embedded; file 
> mini_NASARI.tsv, nel materiale della lezione).
>2. La valutazione della nostra annotazione è condotta calcolando i coefficienti di Pearsons e Separman fra (la media dei) i punteggi annotati a mano e quelli 
> calcolati con la versione embedded di NASARI.

Inizialmente vengono caricati i seguenti file

~~~~python
clocchiatti_score   "./asset/it.test.dataClocchiatti.tsv"
mini_nasari         "./asset/mini_NASARI.tsv"
babelSenses         "./asset/SemEval17_IT_senses2synsets.txt"
~~~~

ottenendo delle liste con la seguente struttura

~~~~python
clocchiatti_score   [["word 1", "word 2", "score"]]
mini_nasari         [[id,word,Nasari [vector]]] where [vector]] is a list of elements
babelSenses         [[word, [babel_id]]] where [babel_id]] is a list of Bebel id
~~~~

<br/>

Il calcolo della similarità tra due termini in base ai vettori Nasari viene fatto con la funzione `getNasariScore()`, la quale chiama inizialmente la funzione `getDictNasariBabel()` per creare i seguenti dizionari:

* `id_word`: dizionario che mappa il babel_id di un elemento con la parola corrispondente;
* `id_vector`: dizionario che mappa il babel_id di un elemento con il vettore Nasari corrispondente.

Questi dizionari risultano utili durante il calcolo della massima similarità tra sensi.

Per ogni coppia `(word1, word2)` della lista `record` viene calcolata la lista di id Babel associati alla parola. La funzione (`getBabelId()`) cicla su tutti gli elementi della lista Babel (`babelSenses`)e ritorna gli id babel riferiti alla parola in input (`word`). Nel caso in cui non ci siano id babel associati alla parola in input, la funzione ritorna una lista vuota.

Una volta calcolate le liste di `babel_id` riferite ad ogni parola della coppia, nel caso in cui queste liste non siano vuote, viene calcolata la similarità massima tra i due termini (`bestSenseSimilarity()`)

* ## bestSenseSimilarity()

Per entrambe le liste di babel_id, viene creata una lista contenente la tupla

~~~~python
(id, vect)
~~~~

Le due liste (`nasariVector_w1`,`nasariVector_w2`) si ottengono tramite

~~~~python
for id in babel_id1:
        vect = id_vect.get(id)
        if vect:
            nasariVector_w1.append((id, vect))
~~~~

Per ogni `babel_id` della lista di una parola si ricava il vettore corrispondente dal `dizionario babel_id-nasari_vecto` (`id_vect`).

<br/>

Per ogni tupla (`vw1`) della lista di tuple `nasariVector_w1` di `word1` e per ogni tupla della lista di `word2`, viene calcolata la Cosine similarity tra i due vettori nasari. La cosine similarity tra due vettori `X` e `Y` si calcola come il prodotto scalare tra i due vettori diviso il prodotto tra la norma 2 di ogni vettore.

~~~~plain
cos_sim (X,Y) =  <X, Y> / (||X||*||Y||)
~~~~

dove:

* `<X, Y> `: prodotto scalare tra i vettori `X` e `Y`
* `||X||`: norma 2 del vettore `X`

Nel codice la cosine similarity viene calcolata nel seguente modo

~~~~python
sim = np.inner(x, y)/(norm(x) * norm(y))
~~~~

La funzione ritorna una lista contenente la coppia di sensi (`babel_id`) che hanno ottenuto il valore di similarità maggiore. La lista quindi ha la seguente composizione:

~~~~python
[babel_id_word1,babel_id_word2, similarity_score]
~~~~

<br/><br/>

Di seguito la tabella che confronta i valori di similarità annotati (normalizzati) con quelli calcolati tramite vettori Nasari

Term 1 | Term 2 | My score | Nasari score
:------------: | :------------: | :-------------: | :-------------:
terremoto | scossa | 0.875 | 0.98
patrimonio | azione | 0.25 | 0.86
ebreo | Gerusalemme | 0.625 | 0.9
nuvolosità | previsione | 0.75 | 0.51
dizionario | enciclopedia | 0.875 | 0.76
zecca | museo | 0.125 | 0.51
sedia | sgabello | 0.875 | 0.96
spagnolo | umidità | 0.0 | 0.42
lattina | bottiglia | 0.875 | 0.89
mosca | formica | 0.75 | 0.9
mito | satira | 0.25 | 0.58
centro della città | autobus | 0.25 | 0.0
coda | Boeing 747-200 | 0.0 | 0.81
opera d'arte | artista | 0.875 | 0.92
NATO | alleanza | 0.5 | 0.66
re | sovrano | 1.0 | 1.0
ritmo | cadenza | 1.0 | 0.89
Alexander Fleming | penicillina | 0.625 | 0.95
flauto | musica | 0.75 | 0.89
airone cenerino | lago | 0.25 | 0.52
viscosità | spruzzo | 0.125 | 0.73
hardware | case | 0.625 | 0.92
anello | fidanzamento | 0.75 | 0.55
latino | tedesco | 0.75 | 0.84
classe operaia | fabbrica | 0.5 | 0.51
Shakespeare | Dickens | 0.5 | 0.77
banconota | prete | 0.0 | 0.33
strumento | lavoro | 0.25 | 0.69
cinghiale nano | suidi | 1.0 | 0.7
suffragio | uscita | 0.0 | 0.39
stella | luminosità | 0.5 | 0.97
trota | chitarra | 0.0 | 0.29
dollaro | milionario | 0.25 | 0.56
cifra | numero | 1.0 | 1.0
burrasca | coperta | 0.0 | 0.47
Obama | Clinton | 0.5 | 0.95
personaggio secondario | film | 0.625 | 0.85
Juventus | Bayern Monaco | 0.625 | 0.87
cambiamento climatico | precipitazione | 0.5 | 0.67
IA | batteria | 0.125 | 0.68
capolavoro | Gioconda | 0.25 | 0.93
crimine | aggressione | 0.5 | 0.92
incoronazione | acqua | 0.0 | 0.49
vocalista | pentagramma | 0.25 | 0.0
spareggio | pallacanestro | 0.625 | 0.68
forze armate | difesa | 0.5 | 0.91
lago | nuvola | 0.125 | 0.52
monastero | doccia | 0.0 | 0.44
lingua madre | lingua | 1.0 | 0.96
porto | incarto | 0.0 | 0.46