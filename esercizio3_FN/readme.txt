————————————————————————————————————————————
Mapping di Frame in WN Synsets
————————————————————————————————————————————


- 'name'       : the name of the Frame (e.g. 'Birth', 'Apply_heat', etc.)
- 'lexUnit'    : a dict containing all of the LUs for this frame.
                     The keys in this dict are the names of the LUs and
                     the value for each key is itself a dict containing
                     info about the LU (see the lu() function for more info.)
- 'FE' : a dict containing the Frame Elements that are part of this frame
             The keys in this dict are the names of the FEs (e.g. 'Body_system')
             and the values are dicts containing the following keys
          - 'definition' : The definition of the FE
          - 'name'       : The name of the FE e.g. 'Body_system'
          - 'ID'         : The id number
          - '_type'      : 'fe'
          - 'abbrev'     : Abbreviation e.g. 'bod'
          - 'coreType'   : one of "Core", "Peripheral", or "Extra-Thematic"
          - 'semType'    : if not None, a dict with the following two keys:
             - 'name' : name of the semantic type. can be used with
                        the semtype() function
             - 'ID'   : id number of the semantic type. can be used with
                        the semtype() function
          - 'requiresFE' : if not None, a dict with the following two keys:
             - 'name' : the name of another FE in this frame
             - 'ID'   : the id of the other FE in this frame
          - 'excludesFE' : if not None, a dict with the following two keys:
             - 'name' : the name of another FE in this frame
             - 'ID'   : the id of the other FE in this frame



0. INDIVIDUAZIONE DI UN SET DI FRAME
________________________________________________________

Come prima operazione ciascuno deve individuare un insieme di frame (nel seguito riferito come FrameSet) su cui deve lavorare.
La funzione restituisce, dato un cognome in input, l'elenco di frame da elaborare. Questo si ottiene tramite 
	getFrameSetForStudent('Clocchiatti')
Ottenendo il seguente set
	
	student: Clocchiatti
        ID:   31        frame: Scrutiny
        ID:  120        frame: Arraignment
        ID: 1030        frame: Remainder
        ID: 1771        frame: Thriving
        ID: 2303        frame: Container_focused_placing


1. ASSEGNAZIONE DI UN WN SYNSET AD UN ELEMENTO FRAMENET
________________________________________________________

Per ogni frame nel FrameSet è necessario assegnare un WN synset ai seguenti elementi: Frame name, Frame Elements (FEs) del frame e Lexical Units (LUs) del frame.
Per ottenere il miglior synset che rappresenta il frame si utilizza la funzione getWNSynset(), la quale necessita di tre input:
	- id: id del frame
	- el: elemento con cui trovare il migliore synset
	- type: tipologia di el (0 - frame name, 1 - frame elements, 2 - lexical units)

L'idea è di calcolare due contesti:
 - contesto relativo al frame
 - contesto relativo al synset
Il synset si basa sul frame name, frame elements e lexical units. Per determinare il synset che rappresenta meglio il frame (mapping migliore) si effettua l'overlap tra i due contesti.

============================
Frame name
============================

Il frame name di un frame id si ottiene tramite funzione getFrameName() (fn.frame_by_id(id)). Nel caso in cui il frame sia una multiword expression (es. Container_focused_placing), è necessario disabituare il termine principale. In generale il termine princiaple è:
	- il sostantivo se l'espressione è composta da NOUN+ADJ
	- il verbo se l'espressione è composta da VERB+NOUN.

***** Disambiguazione
Al momento la funzione di disambiguazione permette di ottenere il pos_tagging (part-of-speech tagging) di una frase e, tramite funzione 
	nltk.pos_tag(nltk.word_tokenize(s), tagset='universal')
si ottiene una lista in cui ogni termine della frase è associata al suo tag.
Per ogni termine della lista (pos_tags), nel caso in cui il suo tag è un verbo o un nome, viene ritornata la parola corrispondente. 


Per ogni frame si ottiene il contesto basato sulla definizione del frame (f.definition) e i synsets riferiti al nome del frame (frame name, el).

Nel caso esista solo un synset riferito al frame name, questo risulta essere per forza il migliore.
Nel caso ci siano più synset, è necessario ciclare su tutti, ottenere il contesto relativo ai synset, ottenere l'overlap tra i due contesti (computeOverlap()) e scegliere (selezionare) come migliore  il synset che ha ottenuto una sovrapposizione maggiore. 
In questo caso il mapping frame-synset avviene con un approccio bag of words.

Il contesto del frame consiste nella definizione (f.definition) pre-processata (rimozione stop-word, ...) del frame.
Il contesto del synset consiste nell'unione delle definizioni e degli esempi del synset e dei suoi iperonimi e iponimi (tutti processati).

***** Overlap (Bag of words)
Lo score di sovrapposizione (overlap) tra i contesti del frame e del synset si ottiene come:
	cardinalità dell'insieme intersezione tra i due contesti + 1

============================
Frame element (FE)
============================

I frame elements di un frame si ottengono tramite la funzione getFrameElements(f) (fn.frame_by_id(id))


Inizialmente viene calcolato il fram e dato l'id, in modo tale da ottenere il contesto del frame

Per ogni frame element (FE) si determinano i WN synset associati e, per ogni synset, si calcola il contesto (getSynsetContext(s)). 
In questo modo si calcola l'overlap tra il contesto del frame e tutti i synset associati ai frame elements del frame. Il synset che ottiene lo score di overlap maggiore risulta essere quello migliore.

============================
Lexical Units (LU)
============================

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
A lexical unit (LU) is a pairing of a word with a meaning. For example, the "Applyheat" Frame 
describes a common situation involving a Cook, some Food, and a Heating Instrument, and is _evoked by words such as bake, blanch, boil, broil, brown, simmer, steam, etc. These frame-evoking words 
are the LUs in the Apply_heat frame. Each sense of a polysemous word is a different LU.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Inizialmente viene calcolato il frame dato l'id, in modo tale da ottenere il contesto del frame (ctx_frame)


Per ogni lexical unit (LU) si prende il nome del lexical unit (tramite lu.lexemes[0].name) e si calcolano i synset associati al nome del lexical unit.
Per ogni synset si calcola il contesto di disambiguazione (getSynsetContext(s)) e si calcola l'overlap con il contesto del frame. Il synset con score overlap maggiore risulta essere il migliore.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Inizialmente calcolavo un synset per ogni elemento del frame (un synset per il frame name, un synset unico per tutti i frame elements, un frame unico per tutte le lexical unit).
Adesso calcolo un synset per ciascun elemento:
 - un synset per il frame name
 - un synset per ogni frame element del frame
 - un sysnet per ogni lexical unit del frame


 





