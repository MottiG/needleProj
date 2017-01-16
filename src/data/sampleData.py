__author__ = 'slouis'

import os
from collections import defaultdict

os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))

outputFilePath = os.path.join(os.getcwd(), 'data', 'interim','patentsMergedFields.txt')

PERCENTS = 0.05   # percents of nodes in the sample
PATENTS_FILE = os.path.join(os.getcwd(), 'data', 'raw','patents.txt')
INVENTORS_FILE = os.path.join(os.getcwd(), 'data', 'raw','inventors.txt')
ABSTRACTS_FILE = os.path.join(os.getcwd(), 'data', 'raw','abstracts.txt')
CITATIONS_FILE = os.path.join(os.getcwd(), 'data', 'raw','citations.txt')

patents_patents = defaultdict(int)
inventors_patents = defaultdict(int)
abstracts_patents = defaultdict(int)
citing_patents = defaultdict(int)
cited_patents = defaultdict(int)

print("Getting PATENTS_FILE")
with open(PATENTS_FILE, encoding="utf8") as vf:
    next(vf)
    for line in vf:

        patents_patents[line.strip().split()[0]]
print(len(patents_patents))

print("Getting INVENTORS_FILE")
with open(INVENTORS_FILE, encoding="utf8") as vf:
    next(vf)
    for line in vf:
        inventors_patents[line.strip().split()[0]]

print(len(inventors_patents))

print("Getting ABSTRACTS_FILE")
with open(ABSTRACTS_FILE, encoding="utf8") as vf:
    next(vf)
    for line in vf:
        abstracts_patents[line.strip().split()[0]]
print(len(abstracts_patents))

print("Getting CITATIONS_FILE")
with open(CITATIONS_FILE, encoding="utf8") as vf:
    next(vf)
    for line in vf:
        citing_patents[line.strip().split()[0]]
        cited_patents[line.strip().split()[0]]
print (len(citing_patents))
print (len(cited_patents))



print ('done!')