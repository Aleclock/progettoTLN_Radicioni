import numpy as np
from scipy.stats import rankdata
from scipy.stats import spearmanr

#class Correlation:

def pearson_index(target, data):
    target = np.array(target).astype(np.float)
    data = np.array(data).astype(np.float)
    
    # la funzione np.cov ritorna un'array del tipo [cov(a,a), cov(a,b), cov(a,b), cov(b,b)], dove a,b: array in input
    return np.cov(target,data)[0][1] / (np.std(target) * np.std(data))

def spearman_index(target, data):
    #ss = spearmanr(target,data)
    target = np.array(rankdata(target)).astype(np.float)
    data = np.array(rankdata(data)).astype(np.float)
    
    return pearson_index(target,data)