————————————————————————————————————————————
NASARI SUMMARIZATION
————————————————————————————————————————————

Inizialmente viene caricato il testo (articolo) e Nasari.
Scelta del metodo (al momento solo "title")

Il riassunto viene invocato tramite la funzione summarization(), la quale prende in input:
 - document_path: percorso del file (per il salvataggio)
 - title: titolo dell'articolo
 - article: articolo diviso in paragrafi
 - nastri: dizionario Nasari
 - compression: indice di compressione

Tramite getNasariVectors() si ottiene una lista di vettori nasari contenente i topic riferiti al titolo (title). 
Per ogni paragrafo dell'articolo (for s in article) viene calcolata la lista di vettori nasari e, per ogni topic del titolo (lista vettori nasari del titolo) e per ogni topic del paragrafo (lista vettori nasari del paragrafo), viene calcolato il Weighted Overlap.

|	Nel caso in cui il riassunto sia basato sul title (title_method), il riassunto 
|	del documento Napoleon non risulta possibile, in quanto non esistono vettori
|	relativi alle parole Napoleon e Bonaparte (sia small che complete Nasari).
|	Risulta necessario utilizzare un'altra versione di small Nasari 
|	(dd-small-nasari-15__.txt)

Weighted Overlap
======================== 
La sovrapposizione pesata (Weighted Overlap) tra i due vettori Nasari (uno del titolo e l'altro del paragrafo) si ottiene determinando inizialmente l'insieme delle chiavi riferite al vettore Nasari (vect.keys()) in comune ai due vettori Nasari. Se l'insieme delle chiavi in comune è maggiore di zero, la sovrapposizione pesata si calcola come rapporto tra:
 - Sommatoria del reciproco della somma tra i rank dei vettore Nasari e q, dove q è la chiave contenuta nell'insieme delle chiavi comuni ai due vettori.
	* La funzione rank determina la posizione della chiave q nel vettore Nasari, in modo tale da determinare quanto quella chiave è rilevante in quel vettore. Questo perché i vettori Nasari sono ordinati in maniera decrescente in base alla rilevanza
 -  Sommatoria di i che va da 1 alla cardinalità dell'insieme delle chiavi in comune, del reciproco del doppio di i
La funzione getWeightedOverlap() ritorna il rapporto se l'insieme delle chiavi in comuni non è vuoto, 0 altrimenti.


Dopo aver calcolato la weighted overlap per tutti per tutti i Nasari vector del titolo dato un Nasari vector dell'articolo, viene fatta la media (diviso per il numero di topic del titolo) dell'overlap parziale rispetto al vettore nasari riferito al paragrafo. La media dell'overlap parziale (topic_wo) viene aggiunta all'overlap totale del paragrafo (sentence_wo).

Se la dimensione del Nasari vector del paragrafo è maggiore di zero, viene fatta la media anche del punteggio del paragrafo (sentence_wo diviso per la dimensione dei topic del paragrafo).


In base al grado di compressione si calcola il numero di paragrafi che è possibile rimuovere (percent). I paragrafi da eliminare sono quelli che, nel calcolo della rilevanza con il titolo, hanno ottenuto il punteggio minore (overlap minore). I paragrafi da eliminare vengono sostituiti con "".
Successivamente viene memorizzato l'articolo riassunto.
	