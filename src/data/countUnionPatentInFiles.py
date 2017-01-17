__author__ = 'slouis'
# Counts unique patent in each file and check the union (to answer the question: How match data do we have?)
import os
from collections import defaultdict

def AllPatents():
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
            l = line.strip().split()
            citing_patents[l[0]]
            cited_patents[l[1]]
    print (len(citing_patents))
    print (len(cited_patents))

    print("Getting PATENETS (excluding cited)")

    finalDict = patents_patents.copy()
    finalDict.update(inventors_patents)
    finalDict.update(abstracts_patents)
    finalDict.update(citing_patents)

    print (len(finalDict))

    print("Getting PATENETS (including cited)")

    finalDict.update(cited_patents)

    print (len(finalDict))


    print ('done!')
    return finalDict

finalPatentDict = AllPatents()

print('')

#  OUTPUTS:
# Getting PATENTS_FILE
# 5759227
# Getting INVENTORS_FILE
# 5759227
# Getting ABSTRACTS_FILE
# 5236725
# Getting CITATIONS_FILE
# 4498006
# 4080259
# Getting PATENETS (excluding cited)
# 5759231
# Getting PATENETS (including cited)
# 5759231
# done!
