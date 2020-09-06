# **Mapping di Frame in WN Synsets**


>
>* 'name'       : the name of the Frame (e.g. 'Birth', 'Apply_heat', etc.) <br/><br/>
>* 'lexUnit'    : a dict containing all of the LUs for this frame. <br/>
>  The keys in this dict are the names of the LUs and the value for each key is itself a dict containing info about the LU (see the lu() function for more info.)<br/><br/>
>* 'FE' : a dict containing the Frame Elements that are part of this frame <br/>
>  The keys in this dict are the names of the FEs (e.g. 'Body_system') and the values are dicts containing the following keys <br/>
>    - 'definition' : The definition of the FE <br/>
>    - 'name'       : The name of the FE e.g. 'Body_system' <br/>
>    - 'ID'         : The id number <br/>
>    - '_type'      : 'fe' <br/>
>    - 'abbrev'     : Abbreviation e.g. 'bod' <br/>
>    - 'coreType'   : one of "Core", "Peripheral", or "Extra-Thematic" <br/>
>    - 'semType'    : if not None, a dict with the following two keys: <br/>
>         - 'name' : name of the semantic type. can be used with the semtype() function
>         - 'ID'   : id number of the semantic type. can be used with the semtype() function
>          - 'requiresFE' : if not None, a dict with the following two keys: <br/>
>    - 'name' : the name of another FE in this frame <br/>
>          - 'ID'   : the id of the other FE in this frame <br/>
>   - 'excludesFE' : if not None, a dict with the following two keys: <br/>
>          - 'name' : the name of another FE in this frame <br/>
>          - 'ID'   : the id of the other FE in this frame <br/>

<br/><br/>

# 0. INDIVIDUAZIONE DI UN SET DI FRAME

Come prima operazione ciascuno deve individuare un insieme di frame (nel seguito riferito come FrameSet) su cui deve lavorare.
La funzione restituisce, dato un cognome in input, l'elenco di frame da elaborare. Questo si ottiene tramite ``getFrameSetForStudent('Clocchiatti')``, ottenendo il seguente set:
	
	student: Clocchiatti
        ID:   31        frame: Scrutiny
        ID:  120        frame: Arraignment
        ID: 1030        frame: Remainder
        ID: 1771        frame: Thriving
        ID: 2303        frame: Container_focused_placing

<br/><br/>

# 1. ASSEGNAZIONE DI UN WN SYNSET AD UN ELEMENTO FRAMENET

Per ogni frame nel FrameSet è necessario assegnare un WN synset in base ai seguenti elementi: Frame name, Frame Elements (FEs) del frame e Lexical Units (LUs) del frame. Per ottenere il miglior synset che rappresenta il frame si utilizza la funzione ``getWNSynset()``, la quale necessita di quattro input:

* id: id del frame;
* el: elemento con cui trovare il migliore synset;
* ctx_frame: contesto del frame;
* type: tipologia di el (0 - frame name, 1 - frame elements, 2 - lexical units).

<br/>

L'idea è di calcolare due contesti:

* contesto relativo al frame;
* contesto relativo al synset.
Il synset si basa sul frame name, frame elements e lexical units e, per determinare il synset che rappresenta meglio il frame (mapping migliore), si calcola l'overlap tra i due contesti.

Il contesto relativo al frame è uguale per qualsiasi elemento ed è basato sui seguenti elementi:

* definizione del frame;
* definizioni dei frame elements;
La lista di parole delle varie definizioni è soggetta a processamento (rimozione stopwords, rimozione punteggiatura, lemmatizzazione).
Invece il contesto del synset viene calcolato ad ogni iterazione ed è composto da:

* definizione del synset;
* esempi del synset;
* iperonimi e iponimi del synset.

<br/>

## Frame name

Il frame name di un frame id si ottiene tramite funzione ``getFrameName()`` (``fn.frame_by_id(id)``). Nel caso in cui il frame sia una multiword expression (es. Container_focused_placing), è necessario disabituare il termine principale. In generale il termine principale è:

* il sostantivo se l'espressione è composta da NOUN+ADJ
* il verbo se l'espressione è composta da VERB+NOUN.

<br/>

* ### *Disambiguazione*

La funzione di disambiguazione permette di ottenere il pos_tagging (part-of-speech tagging) di una frase e, tramite funzione

~~~~python
nltk.pos_tag(nltk.word_tokenize(s), tagset='universal')
~~~~

si ottiene una lista in cui ogni termine della frase è associata al suo tag. Per ogni termine della lista (``pos_tags``), nel caso in cui il suo tag sia un verbo o un nome, viene ritornata la parola corrispondente.

Per ogni frame si determinano i synsets riferiti al nome del frame (``frame name, el``). Nel caso esista solo un synset riferito al frame name, questo risulta essere per forza il migliore.
Nel caso ci siano più synset, è necessario ciclare su tutti, ottenere il contesto relativo ai synset, calcolare l'overlap tra i due contesti (``computeOverlap()``) e scegliere (selezionare) come migliore il synset che ha ottenuto un punteggio di sovrapposizione maggiore.
In questo caso il mapping frame-synset avviene con un approccio **bag of words**.

Come già detto nell'introduzione, il contesto del frame è costituito dalle definizioni (``f.definition, f.FE[fe].definition``) pre-processate del frame e dei frame elments del frame. Il contesto del synset consiste nell'unione delle definizioni e degli esempi del synset e dei suoi iperonimi e iponimi (tutti soggetti a processamento).

<br/>

* ### *Overlap (Bag of words)*

Lo score di sovrapposizione (overlap) tra i contesti del frame e del synset si ottiene tramite la funzione ``computeOverlap()``, la quale calcola:

~~~~plain
cardinalità dell'insieme intersezione tra i due contesti + 1
~~~~

<br/>

## Frame element (FE)

I frame elements di un frame si ottengono tramite la funzione ``getFrameElements(f)`` (``fn.frame_by_id(id)``)

Questa parte ha l'obiettivo di mappare il frame con il synset migliore sulla base del frame element. Il risultato è quindi una lista in cui ogni frame element è associato al suo relativo synset.

Per ogni frame element (FE) si determinano i WN synset associati (``wn.synsets(fe)``) e, per ogni synset, si calcola il contesto del synset (``getSynsetContext(s)``). In questo modo si calcola l'overlap tra il contesto del frame e il contesto del synset. Il synset che ottiene lo score di overlap maggiore risulta essere quello migliore e viene quindi memorizzato insieme al frame element corrispondente.

<br/>

## Lexical Units (LU)

>A lexical unit (LU) is a pairing of a word with a meaning. For example, the "Applyheat" Frame
>describes a common situation involving a Cook, some Food, and a Heating Instrument, and is _evoked by words such as bake, blanch, boil, broil, brown, simmer,steam, etc. These frame-evoking words
>are the LUs in the Apply_heat frame. Each sense of a polysemous word is a different LU.

Questa parte, come la precedente, ha l'obiettivo di mappare un synset al frame in base alla lexical unit del frame.

Per ogni lexical unit (LU) si prende il nome del lexical unit (tramite ``lu.lexemes[0].name``) e si determinano i synset associati al nome del lexical unit.
Per ogni synset si calcola il contesto di disambiguazione (``getSynsetContext(s)``) e si calcola l'overlap con il contesto del frame. Il synset con score overlap maggiore risulta essere il migliore per quella specifica lexical unit.

<br/><br/>

# 2. VALUTAZIONE DELL'OUTPUT DEL SISTEMA

Dopo aver mappato, per ogni frame del frameSet, ogni elemento con il corrispondente synset, il file ``ann_output.txt`` viene aggiornato con i valori del mapping. Ad ogni mapping eseguito, viene scritta sul file la seguente sequenza: <br/>

~~~~plain
type, frame_name, element, synset
~~~~

dove:

* ``type:`` tipologia di elemento (fn: frame name, fe: frame element, lu: lexical unit);
* ``frame_name:`` nome del frame;
* ``element:`` elemento del frame da utilizzare per il mapping;
* ``synset:`` synset associato al frame.

Di seguito un estratto del risultato:

~~~~plain
fn, Scrutiny, Scrutiny, Synset('examination.n.01')
fe, Scrutiny, Cognizer, None
fe, Scrutiny, Ground, Synset('land.n.04')
fe, Scrutiny, Phenomenon, Synset('phenomenon.n.01')
fe, Scrutiny, Manner, Synset('manner.n.01')
fe, Scrutiny, Means, Synset('means.n.01')
~~~~

Il file contentente il mapping generato dal programma (``ann_output.txt``) viene confrontato con il file contentente il mapping generato manualmente (``ann_input.txt``).

<br/>

## Annotazione manuale

L'annotazione manuale prevede il mapping tra il frame e il synset che si considera più appropriato sulla base dell'elementod del frame(frame name, frame element e lexical unit). In questo caso il synset viene scelto tra quelli che il programma valuta (attraverso la funzione ``wn.synsets(fe)``).
Per fare questo mi sono servito di cinque file, uno per ogni frame, in cui vengono elencati tutti gli elementi del frame con i corrispondenti synset. La struttura del documento prevede che, per ogni elemento del frame, ci sia una tabella del tipo

>* ## Beneficiary
>
>> An individual who may use the Remainder for his benefit.  'Is there any food left for me?'
>
>Synset | Score | Best synset | Definition
>------------ | :------------: | :-------------: | -------------
>```Synset('beneficiary.n.01')``` |0.071 | X | the recipient of funds or other benefits
>```Synset('benefactive_role.n.01')``` |0.024 | | the semantic role of the intended recipient who benefits from the happening denoted by the verb in the clause
>```Synset('beneficiary.a.01')``` |0.024 | | having or arising from a benefice

<br/>

Il confronto tra l'annotazione manuale e quella automatica viene fatta grazie alla funzione ``compareAnnotation(ann_in,ann_out)``, la quale valuta se le righe del file (e quindi le associazioni) siano uguali tra loro. La funzione ritorna lo score, calcolato come

~~~~plain
associazioni corrette / numero totale di elementi
~~~~

ottendendo il seguente risultato

~~~~plain
Output evaluation: 0.653
~~~~
