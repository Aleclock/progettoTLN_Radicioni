import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# nltk.download('averaged_perceptron_tagger')

from frameSetStudent import *


"""
Allow to call the correct function based on type variable (frameName, frameElements, lexicalUnits)
Input:
    id: frame id
    el: frame elements (frame name, frame elements, lexical units)
    ctx_frame: context of the frame
    type: type of el element (0: frame name, 1: frame elements, 2: lexical units)
Output:
    best WN synset
"""
def getWNSynset(id, el, ctx_frame, type):
    if (type == 0):
        return syn_frameName(id, ctx_frame, el)
    elif (type == 1):
        return syn_frameElements(id, ctx_frame, el)
    elif (type == 2):
        return syn_lexicalUnits(id, ctx_frame, el)

"""
Calculate the best WN synset of a frame name
Input:
    id: frame id
    ctx_frame: context of frame
    el: frame name
Output:
    best_sense: best WN synset
"""
def syn_frameName(id, ctx_frame, el):

    if "_" in el:   # Disambiguation needed
        pos_tags = getPOS(el)
        el = getMainTerm(pos_tags)

    f = getFrame(id) 

    synsets = wn.synsets(el)

    mapped_el = []

    if (len(synsets) == 1):  # If there is only one synset, it is the best
        mapped_el.append(["fn", f.name, el, synsets[0]])
        return mapped_el
    elif (len(synsets) == 0):
        mapped_el.append(["fn", f.name, el, None])
        return mapped_el

    best_sense = None
    max_overlap = 0

    for s in synsets:
        ctx_synset = getSynsetContext(s)
        overlap = computeOverlap(ctx_frame, ctx_synset) + 1
        if (overlap > max_overlap):
            max_overlap = overlap
            best_sense = s

    mapped_el.append(["fn", f.name, el, best_sense])

    return mapped_el


"""
Calculate the best WN synset of frame elements of frame
Input:
    id: frame id
    ctx_frame: context of frame
    el: frame elements
Output:
    best_sense: best WN synset
"""
def syn_frameElements(id, ctx_frame, el):

    if len(el) == 0:
        return None

    f = getFrame(id)

    mapped_el = []

    for fe in el:   # for each frame element
        synsets = wn.synsets(fe)

        ctx_synset = []
        best_sense = None
        max_overlap = 0

        for s in synsets:
            ctx_synset = getSynsetContext(s)
            overlap = computeOverlap(ctx_frame, ctx_synset) + 1

            if (overlap > max_overlap):
                max_overlap=overlap
                best_sense=s

        mapped_el.append(["fe", f.name, fe, best_sense])

    return mapped_el


"""
Input:
    id : id del frame
    ctx_frame: context of frame
    el : dizionario contenente tutte le lexical unit
Output:
    best_sense : WordNet synset che massimizza i contesti
"""
def syn_lexicalUnits(id, ctx_frame, el):

    if len(el) == 0:
        return None

    f=getFrame(id)

    mapped_el=[]

    for name, lu in el.items():   # Per ogni lexical unit del frame f (name: lexical unit name, lu: lexical unit)
        synsets=wn.synsets(lu.lexemes[0].name)

        ctx_synset=[]
        best_sense=None
        max_overlap=0

        for s in synsets:
            ctx_synset=getSynsetContext(s)
            overlap=computeOverlap(ctx_frame, ctx_synset) + 1

            if (overlap > max_overlap):
                max_overlap=overlap
                best_sense=s

        mapped_el.append(["lu", f.name, lu.lexemes[0].name, best_sense])

    return mapped_el


"""
Calculate the overlap between two context
Input:
    signature: context of frame
    context: context of synset
Output:
    length of intersection
"""
def computeOverlap(signature, context):
    intersection=set(signature).intersection(set(context))
    return len(intersection)


"""
Create the context of a synset
The context include the definition and examples of synset (s) and its hypernyms, hyponyms
Input:
    s: synset
Output:
    context
"""
def getSynsetContext(s):
    context=preProcess(s.definition())

    for e in s.examples():
        context=list(set().union(context, preProcess(e)))

    for hypernym in s.hypernyms():
        context=list(set().union(context, preProcess(hypernym.definition())))
        for e in hypernym.examples():
            context=list(set().union(context, preProcess(e)))

    for hypo in s.hyponyms():
        context=list(set().union(context, preProcess(hypo.definition())))
        for e in hypo.examples():
            context=list(set().union(context, preProcess(e)))

    return context

"""
Calculate the context of frame.
The context is composed of:
    * frame definition
    * frame elements defintion
Input:
    id: id of frame
    LE: frame elements of frame
Output:
    context of frame
"""
def getFrameContext(id, FE):
    context = []
    f=getFrame(id)
    context = list(set().union(context, preProcess(f.definition)))  # Adding frame definition
    for fe in FE:
        context=list(set().union(context, preProcess(f.FE[fe].definition))) # Adding frame element definition

    return context


""" Made the pre-process of a sentence
    - stopword removal
    - puntualization removal
    - lemmatization
Input:
    d: sentence
Output:
    list of words
"""
def preProcess(d):
    stop_words=set(stopwords.words('english'))
    punct={',', ';', '(', ')', '{', '}', ':', '?', '!', '.'}
    wnl=nltk.WordNetLemmatizer()
    ps=PorterStemmer()

    tokens=nltk.word_tokenize(d)
    tokens=list(filter(lambda x: x not in stop_words and x not in punct, tokens))
    tokens=list(set(wnl.lemmatize(t) for t in tokens))
    tokens=list(set(ps.stem(t) for t in tokens))
    return tokens


"""
Allow to determinate the Part-of-Speech of frame name
Input:
    sentence: name
Output:
    pos_tags: part-of-speech tags
"""
def getPOS(sentence):
    s=sentence.replace("_", " ")
    pos_tags=nltk.pos_tag(nltk.word_tokenize(s), tagset='universal')
    return pos_tags


"""
Retrieve the main term from a part-of-speech tagging
Input:
    pos: part-of-speech
Output:
    main term
"""
def getMainTerm(pos):
    for word, tag in pos:
        if tag == "VERB":
            return word
        elif tag == "NOUN":
            return word