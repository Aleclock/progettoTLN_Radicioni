# **Sense identification**

<br/><br/>

# 0. INDIVIDUAZIONE DELLE COPPIE

>Le 50 coppie (sul totale di 500 coppie presenti nel file) sono da individuare sulla base del cognome, tramite la funzione definita nel notebook ``semeval_mapper.ipynb``.

Le coppie individuato dal cognome Clocchiatti sono

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

Uno parte di annotazione è il seguente

~~~~plain
terremoto   scossa	        3.5
patrimonio	azione	        1
ebreo	    Gerusalemme	    2.5
nuvolosità	previsione	    3
dizionario	enciclopedia	3.5
zecca	    museo	        0.5
sedia	    sgabello        3.5
spagnolo	umidità         0
lattina	    bottiglia       3.5
~~~~

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

Per ogni coppia `(word1, word2)` della lista `record` (lista contenente i termini e le annotazioni) viene calcolata la lista di id Babel associati alla parola. La funzione `getBabelId()` cicla su tutti gli elementi della lista `babel` (`babelSenses`) e ritorna gli id Babel riferiti alla parola in input (`word`). Nel caso in cui non ci siano id Babel associati alla parola in input, la funzione ritorna una lista vuota.

Una volta calcolate le liste di `babel_id` riferite ad ogni parola della coppia, nel caso in cui queste liste non siano vuote, viene calcolata la similarità massima tra i due termini (`bestSenseSimilarity()`). Nel caso in cui almeno una delle due liste sia vuota, la similarità tra i due termini è `0`.

* ## bestSenseSimilarity()

Per entrambe le liste di babel_id, viene creata una lista di tuple con forma

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

in cui per ogni `babel_id` della lista di una parola si ricava il vettore corrispondente dal `dizionario babel_id-nasari_vecto` (`id_vect`).

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

La funzione ritorna i `babel_id` dei termini e il rispettivo score di similarità della coppia che ha ottenuto il punteggio di similarità maggiore. L'output sarà composto dalla seguente lista

~~~~python
[babel_id_w1, babel_id_w2, similarity_score]
~~~~

dove:

* `babel_id_w1`: `babel_id` della parola 1
* `babel_id_w2`: `babel_id` della parola 2
* `similarity_score`: score di similarità tra i vettori Nasari corrispondenti ai `due babel_id`


Tornando alla funzione `getNasariScore()`, ovvero quella che calcola gli score di similarità in base ai vettori Nasari, il suo output è una lista (`nasari_score`) di liste contenenti i termini e il corrispondente punteggio di similarità, ovvero

~~~~plain
[[word1, word2, score]]
~~~~

<br/>

Dopo aver calcolato i punteggio di similarità mediante vettori Nasari, vengono estratti dalle liste `clocchiatti_score` e `nasari_score` i punteggi di similarità (si ottiene quindi una lista di valori di similarità). Successivamente le liste vengono normalizzate (`clocchiatti_score` contiene valori compresi nel renge `[0,4]`) e viene calcolato l'indice di correlazione tra i due punteggi in base a Pearson e a Spearman, ottenendo il seguente risultato:

~~~~plain
Pearson index correlation: 0.717
Spearman index correlation: 0.758
~~~~

<br/>

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

<br/><br/>

# 2 VALUTAZIONE ANNOTAZIONE

> Il secondo compito consiste nell’individuare i sensi selezionati nel giudizio di similarità.
>
> * La domanda che ci poniamo è la seguente: quali sensi abbiamo effettivamente utilizzato quando abbiamo assegnato un valore di similarità a una coppia di
> termini (per esempio, società e cultura)?
> * NB: questa annotazione, sebbene svolta successivamente a quella della prima consegna, deve essere coerente con l’annotazione dei punteggi di similarità.
>
>Per risolvere questo compito partiamo dall’assunzione che i due termini funzionino come contesto di disambiguazione l’uno per l’altro.
> L’output di questa parte dell’esercitazione consiste in 2 Babel synset ID e dai termini del synset
>
> * il formato di output è quindi costituito da 6 campi (separatore fra campi ;a tabulazione, mentre usiamo la virgola ‘,’ come separatore all’interno dello
> stesso campo):
>
>~~~~plain
>#Term1 Term2 BS1 BS2 Terms_in_BS1 Terms_in_BS2
> macchina bicicletta bn:00007309n bn:00010248n
> auto,automobile,macchina bicicletta,bici,bike
>~~~~
>
> Calcoliamo nuovamente il livello di agreement nelle annotazioni, questa volta utilizzando il punteggio kappa di Cohen
>
> * Chi usa Python può utilizzare il cohen_kappa_score della libreria sklearn.metrics.
> * Se il gruppo di annotatori è formato da 3 componenti, calcolare la kappa di Cohen per ogni coppia e riportare la media risultante, che sarà il valore 
> sintetico di agreement sulle annotazioni prodotte.
>
> Valutiamo il risultato ottenuto (cioè la coppia dei sensi identificati, e la relativa appropriatezza) in rapporto all’output di un semplice sistema realizzato come segue
>
> * Utilizziamo nuovamente i vettori NASARI (versione densa, embedded) presenti nel file mini_NASARI.tsv, disponibile all’interno del materiale della lezione.
>   * NB: il file contiene soli i vettori per i synset associati ai termini delle coppie; NON tutti i termini delle coppie hanno un vettore...
> * Con tali vettori calcoliamo la coppia di sensi che massimizzano lo score di similarità.
>
>~~~~plain
> c1, c2 = argmax (sim(c1,c2))
>~~~~
>
> Misuriamo in questo caso l’accuratezza sia sui singoli elementi, sia sulle coppie.

<br/>

Nella seconda parte dell'esercitazione si utilizza nuovamente la funzione per il calcolo della similarità tra due termini in base ai vettori Nasari, in quanto la consegna richiede un output del tipo

~~~~plain
[word1, word2, id_sense_word1, id_sense_word2, Terms_in_BS1 Terms_in_BS2]
~~~~

La funzione `getNasariScoreSenses()` permette di ottenere una lista di liste nella forma

~~~~plain
[word1, word2, id_sense_word1, id_sense_word2]
~~~~

Successivamente, la funzione `getBabelTerms()` permette di estrarre i Babel senses (termini) dato un `babel_id`. In particolare la funzione ha l'obiettivo di ritornare una lista con la seguente struttura

~~~~plain
[word1, word2, id_sense_word1, id_sense_word2, Terms_in_BS1 Terms_in_BS2]
~~~~

in cui `Terms_in_BS1` corrispondono ai sensi di Babel che corrispondono al senso migliore (`id_sense_word1`). Per fare questo si utilizza la funzione `extractBabelTermAPI()`, la quale utilizza le API Babel per ottenere i lemmi associati ad uno specifico `babel_id`.

~~~~python
def extractBabelTermAPI(babel_id):
    api = BabelnetAPI('034fb2dd-f5af-4840-aab7-917260affe5c')
    senses = api.get_synset(id=babel_id, targetLang="IT")

    terms = []
    for key,value in senses.items():
        if key == "senses":
            for i in value:
                terms.append(i['properties']['fullLemma'])
    return terms
~~~~

Inizialmente è necessario accedere alle API tramite key, per poi ottenere il le informazioni di un Babel synset dato il suo id. Siccome la funzione `api.get_synset()` ritorna un dizionario, è necessario iterare in modo da ottenere i `[senses]` e successivamente aggiungere alla lista `terms` tutti i lemmi di ogni senso.

Siccome BabelNet permette di effettuare solo 1000 chiamate giornaliere, è stato necessario creare una struttura offline per ottenere la lista dei termini dato il `babel_id`. La lista contenente queste associazioni è `babelInfo_API.txt`, la quale è formata da

~~~~plain
[[id_sense_word1, [Terms_in_BS1]]]
~~~~

Utilizzando questo file è possibile, attraverso la funzione dedicata `extractBabelTerm()`, effettuare la stessa operazione offline.

Dopo aver creato la lista in cui si associa alle parole i migliori sensi (`babel_id`) e i corrispondenti termini, questa viene salvata (`babelList.txt`). Viene salvata anche una versione contenente i valori di similarità (`babelList_score.txt`).

<br/>

L'ultima consegna prevede di calcolare l'agreement nell'annotazione utilizzando il punteggio Kappa di Cohen (si utilizza la funzione presente in `sklearn.metrics`). Per fare questo si utilizzano le due liste contententi i valori di similarità (quelli annotati manualmente e quelli calcolati tramite Cosine similarity) mappati nel range `[0,4]` e convertiti in valori interi.
Il risultato è 

~~~~
Kappa Cohen score : 0.237
~~~~

<br/><br/><br/>

Sitografia:

* <https://github.com/ptorrestr/py_babelnet>
* <https://babelnet.org/guide#access>
* <https://babelnet.org/guide>