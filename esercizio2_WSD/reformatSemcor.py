
import re

"""
Funzione utile a ri-formattare l'xml di semcor
Funzione trovata nello zip scaricabile nel file Cor 3.0 (pagina di nltk) --> http://www.nltk.org/nltk_data/
"""
def reformatSemcor(path):
    c = open(path).read()
    c = re.sub(r'&', r'&amp;', c)
    for i in range(10):
        c = re.sub(r'(<[^>]+=)([^">]+)([ >])', r'\1"\2"\3', c)
    f2 = open(path + ".xml", "w")
    f2.write(c)
    f2.close()