import nltk
import re
import numpy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


"""
__ Summarized the text with title method of Compression
Input
	title: title of the document
	document: rapresentation of the document
	nasari: Nasari dictionary
	compression: percent of reduction
Output
    Summarized text
"""
def summarization(title, article, nasari, compression):
    topics = getNasariVectors(title, nasari)    # Nasari vectors of title

    if len(topics) == 0:
        print ("Impossibile effettuare riassunto, non ci sono topic")
        return article
    
    sentences = []
    sentences_score = []

    sentence_wo = 0     # Sentence weighted overlap
    for s in article:   # For each paragraph in article
        context = getNasariVectors(s, nasari)   # Nasari vectors of paragraph of article
        topics_wo = 0
        for c in context:   # For each topic in Nasari vector of paragraph
            for t in topics:    # For each topic in Nasari vector of title
                topics_wo += getWeightedOverlap(c,t)
            topics_wo /= len(topics)
            sentence_wo += topics_wo

        # This control allow to delete from analysis/summarization sentences (s) with no topic in Nasari vectors
        if len(context) > 0:
            sentence_wo /= len(context)
            sentences.append(s)
            sentences_score.append(sentence_wo)

    percent = int((compression * len(sentences_score))/100) # Number of paragraph to delete
    paragraph_score_sorted = numpy.argsort(sentences_score) # Returns the indices that would sort an array

    i = 0
    while (i < percent):
        #print ("---------- Paragraph removed")
        #print (sentences[paragraph_score_sorted[i]])
        sentences[paragraph_score_sorted[i]]= ""
        i += 1

    article_summ = title + "\n"
    for s in sentences:
        article_summ += s + "\n"

    print ("Final length: " + str(len(article_summ)) + "\n")

    return article_summ

"""
Clear the string in input (lower case, lemmatizer) and create a vector of the word of the string
Input:
    sentence: string
Output:
    vector of words
"""
def clear_sentence(sentence):
    s = re.sub('[^A-Za-z0-9]+', ' ', sentence.lower()) # sentence in lower case
    s_no_copy = set(nltk.word_tokenize(s))
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    s_clear = [lemmatizer.lemmatize(w) for w in s_no_copy if not w in stop_words]
    return s_clear

"""
Create a list of Lexical Nasari vector associated to all words of the topic
Input: 
    sentence: string
    nasari: Nasari dictionary
Output:
    list of Nasari vectors
"""
def getNasariVectors(sentence, nasari):
    topic = clear_sentence(sentence)
    vectors = []
    for word in topic:
        if word in nasari.keys():
            vectors.append(nasari[word])
    return vectors


"""
Allow to calculate the Semantic similarity. Implementation of Weight Overlap (Pilehvar et al.)
Input:
    vect1: Nasari vector (topic)
    vect2: Nasari vector (paragraph)
Output:
    square-rooted Weighted Overlap, or 0
"""
def getWeightedOverlap(vect1, vect2):
    keys_overlap = list(vect1.keys() & vect2.keys()) # keys in common
    if len(keys_overlap) > 0:
        n = sum(1 / (rank(q, list(vect1)) + rank(q, list(vect2))) for q in keys_overlap)
        d = sum(list(map(lambda x: 1 / (2 * x), list(range(1, len(keys_overlap) + 1)))))
        return n/d
    return 0


"""
Input:
    q: key of nasari vector
    v: Nasari vector
Output:
    index of the element q in v
"""
def rank(q, v):
    for i in range(len(v)):
        if v[i] == q:
            return i + 1