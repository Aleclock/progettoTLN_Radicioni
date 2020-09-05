import hashlib
import matplotlib.pyplot as plt
import re

def getList(name, path):
    sx = get_range(name)
    dx = sx+50-1
    intervallo = "" + str(sx) + "-" + str(dx)
    print('{:15}:\tcoppie nell\'intervallo {}'.format(name, intervallo))
    couples = openFile(path, sx-1, dx)
    
    return couples

def get_range(surname):
    #nof_elements = 500
    base_idx = (abs(int(hashlib.sha512(surname.encode('utf-8')).hexdigest(), 16)) % 10)
    idx_intervallo = base_idx * 50+1
    return idx_intervallo

"""
Return list of couples based on interval
Input:
    path: path file
    l_bound: lower bound
    u_bound: upper bound
Output:
    list of 50 elements
"""
def openFile(path, l_bound, u_bound):
    file = open(path,"r",encoding="utf-8")
    file_lines = file.readlines()
    couples = []
    for i in range(l_bound, u_bound):
        token = file_lines[i].replace("\n", "").split("\t")
        couples.append((token[0], token[1]))
    return couples