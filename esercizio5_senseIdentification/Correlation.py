import numpy as np
from scipy.stats import rankdata
from scipy.stats import spearmanr
from scipy.stats import pearsonr

"""
Calculate Pearson correlation
Input:
    target: array of value
    data: list of value
Output:
    correlation index
"""
def pearson_index(target, data):
    target = np.array(target).astype(np.float)
    data = np.array(data).astype(np.float)
    
    # la funzione np.cov ritorna un'array del tipo [cov(a,a), cov(a,b), cov(a,b), cov(b,b)], dove a,b: array in input
    #return round(pearsonr(target,data)[0],3)
    return round(np.cov(target,data)[0][1] / (np.std(target) * np.std(data)),3)

"""
Calculate Spearman correlation
Input:
    target: array of value
    data: list of value
Output:
    correlation index
"""
def spearman_index(target, data):
    target = np.array(rankdata(target)).astype(np.float)
    data = np.array(rankdata(data)).astype(np.float)    
    return round(pearson_index(target,data),3)
    #return round(spearmanr(target,data)[0],3)