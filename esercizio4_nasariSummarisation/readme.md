# **Nasari summarisation**

# *Consegna*

L’esercitazione prevede di implementare un algoritmo estrattivo che permette di ridurre le dimensioni del documento del 10, 20 e 30% seguendo i seguenti step:

1. Individuazione dell’argomento (topic) del testo da riassumere. L’argomento può essere indicato come un insieme di vettori Nasari.
𝑉𝑡' ={𝑡𝑒𝑟𝑚'_𝑠𝑐𝑜𝑟𝑒,𝑡𝑒𝑟𝑚(_𝑠𝑐𝑜𝑟𝑒,...,𝑡𝑒𝑟𝑚'4_𝑠𝑐𝑜𝑟𝑒 } 𝑉𝑡( ={𝑡𝑒𝑟𝑚'_𝑠𝑐𝑜𝑟𝑒,𝑡𝑒𝑟𝑚(_𝑠𝑐𝑜𝑟𝑒,...,𝑡𝑒𝑟𝑚'4_𝑠𝑐𝑜𝑟𝑒 }
2. Creazione del contesto, raccogliendo i vettori dei termini (questo passaggio può essere ripetuto, scaricando il contributo dei termini associati ad ogni ciclo);
3. Conservare i paragrafi contenenti i termini più salienti in base alla Weighted Overlap WO(v1, v2) Determinare il peso dei paragrafi applicando almeno uno degli approcci citati (titolo, spunto, frase, coesione).

Vengono forniti due file Nasari:

* dd-nasari.txt , un sottoinsieme di NASARI (ottenuto troncando i vettori a 10 caratteristiche). 3.587.754 vettori, ~ 600 MB (https://goo.gl/85BubW);
* dd-small-nasari-15.txt , un sottoinsieme di NASARI. È stato applicato lo stesso filtro di dd-nasari.txt, con
15 caratteristiche più l’intersezione con i lemmi 60K nel Corpus of Contemporary American English:
13.084 vettori, 2MB di archiviazione (in questo file molte entità sono state rimosse).
Il secondo file è stato estratto per iniziare la nostra sperimentazione, mentre il secondo ha lo scopo di esplorare la risorsa in maniera più approfondita.

I documenti da riassumere sono:

* Andy-Warhol.txt
* Ebola-virus-disease.txt
* Life-indoors.txt
* Napoleon-wiki.txt

Effettuare delle sperimentazioni con diversi livelli di compressione (10%, 20% 𝑒 30%).

<br/><br/>

# 0. Summarisation

L'algoritmo sviluppato determina la rilevanza del testo in base al contesto del titolo (title method).

L'operazione di sintesi viene fatta dalla funzione summarisation(), la quale richiede i seguenti input:

* ``title``: titolo del documento
* ``article``: articolo diviso in paragrafi (lista di stringhe)
* ``nasari``: dizionario Nasari
* ``compression``: tasso di compressione

Per determinare il contesto del titolo si utilizza la funzione ``getNasariVectors()``, con la quale si ottiene una lista di vettori Nasari contenente i topic riferiti al titolo (title).

Per ogni paragrafo dell'articolo (``for s in article``) si determinare il contesto del paragrafo (tramite funzione ``getNasariVectors()``) e, per ogni topic del paragrafo (lista vettori nasari del paragrafo) e per ogni topic del titolo (lista vettori nasari del titolo), viene calcolato la Weighted Overlap.

ATTENZIONE: utilizzando il dizionario Nasari *nasariSubset/dd-small-nasari-15.txt* e *dd-nasari.txt* non è possibile effettuare il riassunto del documento 
*Napoleon-wiki.txt* (utilizzando il metodo basato sul titolo), in quanto non esistono vettori Nasari che corrispondono ai termini Napoleon e Bonaparte.
Per risolvere il problema si utilizza il dizionario *nasariSubset/dd-small-nasari-15__.txt*, il quale contiene i vettori Nasari corrispondenti.

La sovrapposizione pesatea (Weighted Overlap) tra due vettori Nasari (uno riferito al titolo e l'altro al paragrafo) si ottiene determinando inizialmente l'insieme delle chiavi riferite al vettore Nasari (``vect.keys()``) in comune ai due vettori Nasari. Se l'insieme delle chiavi in comune non è vuoto, la sovrapposizione pesata si calcola come rapporto tra:

* Sommatoria del reciproco della somma tra i rank dei vettore Nasari e q, dove q è la chiave contenuta nell'insieme delle chiavi comuni ai due vettori.
  * La funzione rank determina la posizione della chiave q nel vettore Nasari, in modo tale da determinare quanto quella chiave è rilevante in quel vettore. Questo perché i vettori Nasari sono ordinati in maniera decrescente in base alla rilevanza
* Sommatoria di i che va da 1 alla cardinalità dell'insieme delle chiavi in comune, del reciproco del doppio di i
La funzione getWeightedOverlap() ritorna il rapporto se l'insieme delle chiavi in comuni non è vuoto, 0 altrimenti.)

Dopo aver calcolato la weighted overlap per tutti per tutti i Nasari vector del titolo dato un Nasari vector dell'articolo, viene fatta la media (diviso per il numero di topic del titolo) dell'overlap parziale rispetto al vettore nasari riferito al paragrafo. La media dell'overlap parziale (``topic_wo``) viene aggiunta all'overlap totale del paragrafo (``sentence_wo``).

Se la dimensione del Nasari vector del paragrafo è maggiore di zero, viene fatta la media anche del punteggio del paragrafo (``sentence_wo`` diviso per la dimensione dei topic del paragrafo).

In base al grado di compressione si calcola il numero di paragrafi che è possibile rimuovere (``percent``). I paragrafi da eliminare sono quelli che, nel calcolo della rilevanza con il titolo, hanno ottenuto il punteggio minore (overlap minore). I paragrafi da eliminare vengono sostituiti con "".
Infine viene memorizzato l'articolo riassunto.
