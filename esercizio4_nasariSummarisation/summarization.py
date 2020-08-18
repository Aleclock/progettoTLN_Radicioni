import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

"""
__ Summarized the text with title method of Compression%
Input
    path: ouput file path
	title: title of the document
	document: rapresentation of the document
	nasari: Nasari dictionary
	compression: percent of reduction
Output
    Summarized text
"""
def summarization(path, title, article, nasari, compression):
    topics = getNasariVectors(title, nasari)
    print (topics)
    for s in article:
        context = getNasariVectors(s, nasari)
        
    return article
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
Create a list of Nasari vectors from title words token
Input:
    title: title of the document
    nasari: Nasari dictionary
Output:
    list of Nasari vectors
"""
def title_method(title, nasari):
    tokens = clear_sentence(title)
    vectors = getVectors(tokens, nasari)
    return vectors