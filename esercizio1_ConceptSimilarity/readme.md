# **Mapping di Frame in WN Synsets**

# *Consegna*

1. L'input per questa esercitazione è costituito da coppie di termini contenute nel file *WordSim353* (disponibile nei formati .tsv e .csv)
Il file contiene 353 coppie di termini utilizzati come testset in varie competizioni internazionali
A ciascuna coppia è attribuito un valore numerico [0,10], che rappresenta la similarità fra gli elementi della coppia.
2. L'esercitazione consiste nell'implementare tre misure di similarità basate su WordNet.
per ciascuna di tali misure di similarità, calcolare gli indici di correlazione di Spearman and gli indici di correlazione di Pearson fra i risultati ottenuti e quelli ‘target’ presenti nel file annotato.

Le misure di similarità sono:

* ### Wu & Palmer
  * La misura di similarity di Wu & Palmer si basa sulla struttura di WordNet.
  * ``LCS`` è il primo antenato comune (Lowest Common Subsumer) fra i sensi s1 e s2; e depth(x) è una funzione che misura la distanza fra la radice di WordNet e il synset ``x``.

~~~~plain
cs (s1, s2) = 2 * depth(LCS) / (depth(s1) + depth(s2))
~~~~

* ### Shortest Path

  * ``depthMax`` è un valore fisso (TODO mettere formula).
  * La similarità tra i due sensi (``s1,s2``) è funzione del percorso più corto tra i due sensi (``len(s1,s2)``).
    * se ``len(s1,s2) = 0``, ``sim_path(s1,s2)`` ottiene il massimo valore (``2*depthMax``);
    * se ``len(s1,s2) = 2*depthMax``, ``sim_path(s1,s2)`` ottiene il minimo valore (``0``);
    * quindi il valore di ``sim_path(s1,s2)`` è compreso tra ``0`` e ``2*depthMax``.

~~~~plain
sim_path(s1,s2) = 2 * depthMax - len(s1,s2)
~~~~

* ### Leakcock & Chodorow

  * quando ``s1`` e ``s2`` hanno lo stesso senso, ``len(s1,s2) = 0``. A livello pratico, si aggiunge ``1`` sia a ``len(s1,s2)`` sia a ``2*depthMax`` in modo da evitare ``log(0)``
  * Quindi il valore di ``simLC(s1,s2)`` è compreso nell'intervallo ``(0, log(2 * depthMax + 1))``

~~~~plain
simLC(s1,s2) = - log(len(s1,s2) / (2 * depthMax))
~~~~

<br/>

**ATTENZIONE**: l’input è costituito da coppie di termini, mentre la formula utilizza sensi. <br/>

Per calcolare la similarity fra 2 termini immaginiamo di prendere la massima similarity fra tutti i sensi del primo termine e tutti i sensi del secondo termine.

* l’ipotesi è cioè che i due termini funzionino come contesto di disambiguazione l’uno per l’altro.
* nella formula ``c`` sono i concetti che appartengono ai synset associati ai termini ``w1`` e ``w2``.

~~~~plain
sim(w1,w2) = max [sim(x2,c2)]
~~~~

<br/><br/>

# 0. Misure di similarità

Inizialmente viene caricato il csv (``WordSim353.csv``) come una lista e viene creato un dizionario (``similarities``) con la seguente struttura:

~~~~plain
similarities = {
        'Term 1': [],
        'Term 2': [],
        'Target': [],
        'wup': [],
        'sp': [],
        'lch': []
}
~~~~

Per ogni elemento della lista di coppie di termini (``couple_list``), vengono calcolati i synset associati ai due termini

~~~~python
ss1 = wn.synsets(r[0])
ss2 = wn.synsets(r[1])
~~~~

Successivamente viene calcolata la similarità tra i termini utilizzando le rispettive liste di synset. Le funzioni che si utilizzano sono

~~~~python
sim_wup = mm.wuPalmerMetric(ss1, ss2)           #Wu & Palmer
sim_path = mm.shortestPathMetric(ss1, ss2)      #Shortest Path
sim_lc = mm.leakcockChodorowMetric(ss1, ss2)    #Leakcock & Chodorow
~~~~

<br/>

## Wu & Palmer

La funzione ``wuPalmerMetric(ls1, ls2)`` prende in input le liste di synset dei due termini. <br/>
Per ogni synset del primo termine e per ogni synset del secondo, viene calcolato inizialmente il primo antenato comune (Lowest Common Subsumer) tra i due sensi (``getLowestCommonSubsumer()``). Nel caso in cui non ci sia antenato comune, la similarità è ``0``, altrimenti si calcola, tramite ``depthPath(x)``, la distanza fra la radice di WordNet e il synset ``x``. In questo caso sono necessarie tre distanze:

~~~~python
lcs_depth = depthPath(lcs, lcs)
ss1_depth = depthPath(ss1, lcs)
ss2_depth = depthPath(ss2, lcs)
~~~~

Dopo aver calcolato le distanze, la similarità tra i due sensi si calcola come

~~~~plain
similarity (s1, s2) = 2 * lcs_depth / (ss1_depth + ss2_depth)
~~~~

Il valore di similarità ottenuto viene confrontato con il massimo valore corrente, in modo da selezionare il valore maggiore tra i due.

<br/>

## Shortest Path

La funzione ``shortestPathMetric(ls1, ls2)`` prende in input le liste di synset dei due termini. <br/>
La profondità massima (``maxDepth``) viene settata a ``20``, calcolabile con la seguente funzione

~~~~python
def maximimDepth():
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())
~~~~

Per ogni synset del primo termine e per ogni synset del secondo, viene calcolato il percorso più corto (``depth = shortestPath(ss1,ss2)``) tra i due sensi. Se non esiste una distanza tra i due sensi, la similarità è ``0``, altrimenti viene calcolata come

~~~~plain
similarity (s1, s2) = 2 * maxDepth - depth 
~~~~

Il valore di similarità ottenuto viene confrontato con il massimo valore corrente, in modo da selezionare il valore maggiore tra i due.

Siccome il range di similarità è ``[0, 2 * maxDepth]``, il massimo valore di similarità ottenuto viene diviso per ``2 * maxDepth``

<br/>

## Leakcock & Chodorow

La funzione ``leakcockChodorowMetric(ls1, ls2)`` prende in input le liste di synset dei due termini. <br/>
Come nel calcolo precedente, la profndità massima (``maxDepth``) viene settata a ``20``.

Per ogni synset del primo termine e per ogni synset del secondo, viene calcolato il percorso più corto (``depth = shortestPath(ss1,ss2)``) tra i due sensi. La similarità viene calcolata come

~~~~plain
similarity (s1, s2) = log ((depth or 1.) / (2*maxDepth))
~~~~

dove ``depth`` diventa 1 se nullo.

Il valore di similarità ottenuto viene confrontato con il massimo valore corrente, in modo da selezionare il valore maggiore tra i due.

<br/><br/>

# 1. Utils

Di seguito vengono spiegate le funzioni utilizzate per il calcolo della similarità nelle tre metriche.

<br/>

## getCommonSubsumer()

>**Input:**
>
>* ``ss1:`` synset 1
>* ``ss2:`` synset 2
>
>**Output** 
>
>* ``commons_hypernyms:`` lista di iperonimi in comune

<br/>

Inizialmente viene calcolato, per ogni synset, il percorso/lista di percorsi (``hp1``e``hp2``) tra il synset e root, attraverso la funzione ``ss1.hypernym_paths()``. Citando la documentazione
> Get the path(s) from this synset to the root, where each path is a list of the synset nodes traversed on the way to the root.<br/>
>:return: A list of lists, where each list gives the node sequence connecting the initial ``Synset`` node and a root node.
Questa funzione ritorna tutti i path dal ``root`` al ``synset``, quindi dall'elemento più generico al synset che si sta analizzando (più specifico)

<br/>

Per ogni path della lista di path del primo synset (``hp1``) e per ogni percorso della lista di path del secondo synset (``hp2``), le due liste vengono unite in una lista di tuple, in modo da ottenere una struttura del tipo

~~~~plain
[ (nodo_path_synset1 , nodo_path_synset2) ]
~~~~

Per ogni elemento della tupla

* Se i due elementi sono uguali (``nodo_path_synset1 == nodo_path_synset2``), il valore del antenato comune (``common``) viene aggiornato se non già presente nella lista totale di synset comuni (``commons_hypernyms``);
* Se i due elementi sono diversi, il ciclo sugli elementi della tupla viene bloccato in quanto c'è divergenza tra i due percorsi.

<br/>

La lista degli iperonimi in comune ai due synset (``commons_hypernyms``) ha una struttura del tipo:

~~~~plain
[(Synset('abstraction.n.06'), 1)]
~~~~

dove il primo elemento è il synset e il secondo (``1 in questo caso``) si riferisce alla profondità nel path.

<br/>

Siccome la versione precedente non funzionava correttamente, ne ho sviluppata un'altra utilizzando la funzione nltk ``ss1._all_hypernyms``, la quale ritorna tutti gli iperonimi di un synset. Calcolando gli iperonimi di entrambe i synset, è possibile ottenere gli iperonimi comuni facendo l'intersezione tra le due liste

~~~~python
ah1 = ss1._all_hypernyms  # all hypernym
ah2 = ss2._all_hypernyms  # all hypernym
comm = list(ah1.intersection(ah2))
~~~~

<br/>

## getLowestCommonSubsumer()

>**Input:**
>
>* ``ss1:`` synset 1
>* ``ss2:`` synset 2
>
>**Output**
>
>* ``lcs`` primo antenato comune (lowest common subsumer)

<br/>

Inizialmente viene calcolata la lista degli iperonimi comuni ai due synset (``common_hypernyms``) e viene ordinata in base alla profondità del synset comune.
Se non ci sono elementi nella lista (``len(common_hypernyms) == 0``), viene ritornato ``None``, altrimenti viene ritornato il synset del primo elemento della lista, ovvero quello con profondità maggiore.

### **ATTENZIONE** <br/>
Dalle mie analisi questa funzione ritorna lo stesso risultato della funzione embedded di NLTK ``ss1.lowest_common_hypernyms(ss2)``. Solo in un caso il risultato è diverso, in quanto le liste che si ottengono sono

~~~~python
# Synset('space.n.02') Synset('chemistry.n.02')
[Synset('abstraction.n.06'), Synset('physical_entity.n.01')] #NLTK lowest_common_hypernyms(ss2)
[(Synset('abstraction.n.06'), 1), (Synset('physical_entity.n.01'), 1), (Synset('entity.n.01'), 0)] # getLowestCommonSubsumer()
~~~~

In questo caso entrambi i synset hanno lo stesso valore di profondità, quindi l'errore dipende da un ordinamento diverso

<br/>

Siccome ho cambiato la funzione ``getCommonSubsumer()``, è necessario cambiare anche questa funzione. Inizialmente si calcolano gli iperonimi comuni ai due synset. Successivamente, per ogni iperonimo comune, il lcs (least common subsumer) è l'elemento della lista che ha il path (synset - root) più lungo. Questo si ottiene con la funzione ``max_depthPath()``.

~~~~python
def max_depthPath(synset):
    paths = synset.hypernym_paths()
    depth = (max(len(path) for path in paths))
    return depth
~~~~

La funzione ritorna la lunghezza del percorso più lungo tra tutti quelli di un iperonimo (``synset.hypernym_paths()``)
<br/>

## shortestPath()

Questa funzione calcola il percorso più corto tra i due synset dati in input. <br/>

* ### **Versione personale con errori**

Inizialmente calcola la lista di iperonimi in comune ai due synsets (``cs``) e, nel caso in cui non ci siano antenati comuni, non esiste un percorso possibile tra i due synsets (ritorna ``None``). Per ogni synset, utilizzando la funzione ``ss1.hypernym_paths()``, viene calcolata la lista di percorsi tra il synset e il root. Attraverso la funzione

~~~~python
list(filter(lambda x: lcs in x, path_s1))
~~~~

vengono mantenute solo le liste che contengono il lowest common subsumer (``lcs``). Questo viene calcolato ordinando cs in base alla profondità e selezionando l'ultimo elemento.

Per ogni path del primo synset e per ogni path del secondo, vengono calcolate due distanze:

* distanza tra il ``path`` (invertito) del primo synset e ``lcs``;
* distanza tra il ``path`` (invertito) del secondo synset e ``lcs``. <br/>
L'inversione della lista permette di ordinarla in modo tale che i primi elementi siano i più specifici e gli ultimi i più generici.  

Questa operazione viene fatta dalla funzione ``getSubDistance(path, lcs)`` la quale confronta ogni elemento con la lista con il synset hcs (highest common subsumer). Appena il confronto ha successo (i due synset sono uguali), viene ritornato l'indice del synset della lista. In questo modo è possibile determinare la distanza tra il synset di partenza e il synset comune ad entrambi. <br/>

Calcolando questa distanza per entrambi i path/synset è possibile determinare la distanza tra i due synset. Siccome è necessario trovare il percorso più corto, viene valutata la lunghezza del percorso attuale con quella minima trovata nei cicli precedenti.

~~~~python
minDist = min(minDist, (d1+d2))
~~~~

Infine viene ritornato il valore della distanza più breve tra i due synset.

* ### **Versione NLTK (shortest_path_distance())**

Siccome la funzione da me implementata dà risultati diversi rispetto a quella implementatta da NLTK, di seguito illustro il funzionamento della funzione ``shortest_path_distance()`` di NLTK.

> ``shortest_path_distance()`` :Returns the distance of the shortest path linking the two synsets (if one exists). For each synset, all the ancestor nodes and 
> their distances are recorded and compared. The ancestor node common to both synsets that can be reached with the minimum number of traversals is used. If no 
> ancestor nodes are common, None is returned. If a node is compared with itself 0 is returned.

*Il problema della mia funzione è che la lista dei percorsi di iperonimi (``hypernym_paths()``) non risulta uguale a ``_shortest_hypernym_paths()``, dando risultati diversi*

Inizialmente viene calcolata la lista dei percorsi degli iperonimi più corti dato un synset (``_shortest_hypernym_paths()``). L'output di questa funzione è un dizionario composto da coppie ``(synset, depth)``. Per ogni elemento (synset) del dizionario relativo al primo synset, viene cercato lo stesso elemento nel dizionario del secondo synset. Nel caso in cui ci sia corrispondenza, ovvero se il synset risulta essere un antenato comune, la distanza tra i due synset originali è data dalla somma tra la profondità (``depth``) dei due elementi. La funzione ritorna la distanza (``d1 + d2``) minore.

<br/>

## depthPath()

Questa funzione permette di calcolare la distanza/lunghezza minima del percorso tra il synset in input e root. 
Inizialmente calcola tutti i path disponibili dato il synset (``hypernym_paths()``) e successivamente la funzione ritorna la lunghezza (``len(path)``) tra i percorsi disponibili. 

<br/><br/>

# 2. Indici di correlazione

Dopo aver calcolato la similarità tra le parole mediante le tre metriche, è necessario calcolare gli indici di correlazione di Spearman and gli indici di correlazione di Pearson fra i risultati ottenuti e quelli ‘target’ presenti nel file annotato. Per fare questo si utilizzano le funzioni ``pearson_index()`` e ``spearman_index()``.

* ##  pearson_index()

> L'indice di correlazione di Pearson è definita come la covarianza tra le due variabili diviso per il prodotto delle loro deviazioni standard.
>
> ~~~~plain
> ρ = cov(X,Y) / (σX * σY)
> ~~~~

Inizialmente entrambe le liste (``target`` e ``data``) vengono convertite in array di ``float``

~~~~python
np.array(data).astype(np.float)
~~~~

La funzione ritorna

~~~~python
np.cov(target,data)[0][1] / (np.std(target) * np.std(data))
~~~~

Siccome la funzione np.cov() ritorna una matrice 2x2 con la forma

~~~~plain
cov(a,a), cov(a,b),
cov(a,b), cov(b,b)
~~~~

è necessario prendere il secondo elemento della prima riga.

<br/>

* ##  spearman_index()

> L'indice di correlazione di Spearman è definita come la correlazione di Pearson applicato ai ranghi (rank) delle variabili.
>
> ~~~~plain
> r = ρ(rgX,rgY) = cov(rgX,rgY) / (σ_rgX * σ_rgY)
> ~~~~

dove:

- r: correlazione di Spearman
- ρ: correlazione di Pearson
- rgX/rgY: rango/rank della variabile X/Y
- σ_rgX/σ_rgY: deviazione standard del rank

Calcola il rank delle liste in input con la funzione ``scipy.stats rankdata()`` e ritorna la correlazione di Pearson applicata ai rank.

<br/><br/>

La correlazione ottenuta con i risultati target e quelli relativi alle metriche NLTK è la seguente

Similarity index | Spearman index | Pearson index |
------------ | :------------: | :-------------:
| | 
**PERSONAL / TARGET** | |
| |
Wu & Palmer | 0.288 | 0.337
Shortest Path | 0.165 | 0.289
Leakcock & Chodorow | 0.318 | 0.289
| |
| **PERSONAL / NLTK** |
| |
Wu & Palmer | 0.993 | 0.994 |
Shortest Path | 0.646 | 0.956 |
Leakcock & Chodorow | 0.984 | 0.992
