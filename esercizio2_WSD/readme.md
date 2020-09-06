# **Word Sense Disambiguation**

# *Consegna*

Implementare l’algoritmo di Lesk (!= usare implementazione esistente, e.g., in nltk...).

1. Disambiguare i termini polisemici all’interno delle frasi del file ‘sentences.txt’; oltre a restituire i synset ID del senso (appropriato per il contesto), il programma deve riscrivere ciascuna frase in input sostituendo il termine polisemico con l’elenco dei sinonimi eventualmente presenti nel synset.
2. Estrarre 50 frasi dal corpus SemCor (corpus annotato con i synset di WN) e disambiguare almeno un sostantivo per frase. Calcolare l’accuratezza del sistema implementato sulla base dei sensi annotati in SemCor.

- SemCor è disponibile all’URL <http://web.eecs.umich.edu/~mihalcea/downloads.html>

<br/><br/>

# PARTE 1 - Disambiguare i termini polisemici all’interno delle frasi (sentences.txt)

Inizialmente viene caricato il file ``sentences.txt``) e, per ogni frase contenuta nel file, viene calcolato il miglior senso best_sense (funzione lesk()), vengono calcolati i sinonimi del miglior senso (funzione findSynonym(best_sense)) e viene memorizzata la frase in modo tale che il termine sia sostituito dai sinonimi del miglior senso. Di seguito il risultao (file ``outputDisambiguation.csv``)

Original sentence | Word | Synset | New sentence
------------ | :------------: | :-------------: | ------------ |
arms bend at the elbow | arms | ``Synset('arm.n.01')`` | ['arm'] bend at the elbow
germany sells arms to saudi arabia | arms | ``Synset('arm.n.02')`` | germany sells ['arm', 'branch', 'limb'] to saudi arabia
the key broke in the lock | key | ``Synset('key.v.02')`` | the ['key'] broke in the lock
the key problem was not one of quality but of quantity | key | ``Synset('key.v.05')`` | the ['key'] problem was not one of quality but of quantity
work out the solution in your head | solution | ``Synset('solution.n.01')`` | work out the ['solution'] in your head
heat the solution to 75¬∞ celsius | solution | ``Synset('solution.n.01')`` | heat the ['solution'] to 75¬∞ celsius
the house was burnt to ashes while the owner returned | ashes | ``Synset('ash.n.03')`` | the house was burnt to ['ash'] while the owner returned
this table is made of ash wood | ash | ``Synset('ash.n.03')`` | this table is made of ['ash'] wood
the lunch with her boss took longer than she expected | lunch | ``Synset('lunch.n.01')`` | the ['lunch', 'luncheon', 'tiffin', 'dejeuner'] with her boss took longer than she expected
she packed her lunch in her purse | lunch | ``Synset('lunch.n.01')`` | she packed her ['lunch', 'luncheon', 'tiffin', 'dejeuner'] in her purse
the classification of the genetic data took two years | classification | ``Synset('categorization.n.03')`` | the ['categorization', 'categorisation', 'classification', 'compartmentalization', 'compartmentalisation', 'assortment'] of the genetic data took two years
the journal science published the classification this month | classification | ``Synset('categorization.n.03')`` | the journal science published the ['categorization', 'categorisation', 'classification', 'compartmentalization', 'compartmentalisation', 'assortment'] this month
his cottage is near a small wood | wood | ``Synset('wood.n.08')`` | his cottage is near a small ['wood']
the statue was made out of a block of wood | wood | ``Synset('wood.n.08')`` | the statue was made out of a block of ['wood']

<br/>

## Lesk

La funzione ``lesk()`` calcola inizialmente il contesto della frase (``sentence``) tramite la funzione ``bagOfWord()``, la quale trasforma la frase in input in base all'approccio bag of words, applicando:

* tokenizzazione;
* rimozione stopwords e punteggiatura;
* lemmatizzazione.

Per ogni senso associato al termine da disambiguare (ottenuto tramite ``wn.synsets(word)``) si calcola il contesto del senso, il quale è composto dalla definizione del senso e dai suoi esempi (ottenuti tramite ``sense.definition()`` e ``sense.examples()``)

La sovrapposizione tra i due contesti si calcola con la funzione ``computeOverlap(signature, context)``, la quale determina la dimensione dell'insieme intersezione tra i due contesti. Il miglior senso è quello che ottiene un overlap maggiore.

<br/>

## FindSynonym

Per ottenere la lista dei sininomi (``findSynonym()``) di un senso si utilizzano le seguenti funzioni

~~~~python
synonyms = []
for l in sense.lemmas():
    synonyms.append(l.name())
return synonyms
~~~~

Lo stesso risultato può essere ottenuto attraverso la funzione ``sense.lemma_names()``, la quale ritorna direttamente la lista dei lemmi dei sinonimi.

<br/><br/>

# PARTE 2 - Disambiguare i termini polisemici all’interno delle frasi Semcor

Inizialmente viene caricato l'XML Semcor (la prima volta è necessario ri-formattarlo con la funzione ``reformatSemcor()`` per poterlo leggere) e vengono selezionate 50 frasi casuali. Per ogni frase vengono selezionati solo i sostantivi validi

~~~~python
tagged_words = [word for word in s.iter()
                  if word.get("cmd") is not "ignore" and
                  word.get("lexsn") is not None and
                  word.get("lemma") is not None and
                  word.get("pos") in ['NN', 'NNS', 'NNPS'] and
                  word.get("wnsn") != "0"]
~~~~

e viene scelto casualmente un termine (dalla lista ``tagged_words``).

Siccome l'obiettivo di questa parte dell'esercitazione è valutare l'efficacia dell'algoritmo di Lesk, si determina il senso del termine scelto in base all'annotazione Semcor

~~~~python
semCorSynset = wn.synset_from_sense_key("%".join([word.get("lemma"), word.get("lexsn")]))   # Synset annotate in semCor
~~~~

La funzione wn.synset_from_sense_key() permette di ottenere il synset a partire dalla chiave di senso, la quale ha la seguente struttura:

~~~~plain
lemma % lex_sense
Esempio: highway%1:06:00:: , state%1:14:01::
~~~~

Il miglior senso viene poi calcolato sia con l'algoritmo di Lesk illustrato precedentemente sia con quello implementato da NLTK.

Di seguito un estratto del file ``outputSemcor.csv`` contentente la frase, il termine da disambiguare e i vari sensi.

Sentence | Ambiguous term | Semcor synset | My synset | NLTK synset
------------ | :------------: | :-------------: | :-------------: | :-------------:
The Highway_Department source told The_Constitution , however , that Vandiver has not been consulted yet about the plans to issue the new rural roads bonds. | source | ``Synset('beginning.n.04')`` | ``Synset('beginning.n.04')`` | ``Synset('source.n.07')``
Nevertheless , '' we feel that in_the_future Fulton_County should receive some portion of these available funds '' , the jurors said. | funds | ``Synset('investment_company.n.01')`` | ``Synset('store.n.02')`` | ``Synset('store.n.02')``
It urged that the city '' take steps to remedy '' this problem . | city | ``Synset('city.n.01')`` | ``Synset('city.n.01')`` | ``Synset('city.n.03')``
It urged that the next Legislature '' provide enabling funds and re-set the effective date so_that an orderly implementation of the law may be effected '' ." | date | ``Synset('date.n.08')`` | ``Synset('date.n.07')`` | ``Synset('go_steady.v.01')``

<br/>

Infine l'accuratezza della disambiguazione viene calcolato con la funzione ``accuracy_score`` della libreria ``sklearn.metrics``. Siccome le frasi e i termini da disambiguare vengono cambiati ad ogni esecuzione, non è possibile determinare un valore preciso di accuratezza. In ogni caso l'accuratezza dell'algoritmo sviluppato ottiene risultati molto simili rispetto a quelli ottenuti dall'algoritmo di Lesk NTLK. In generale l’accuratezza dell’annotazione effettuata rispetto a quella di Semcor risulta essere compresa tra il 30% e il 50%.