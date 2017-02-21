import os
from collections import defaultdict
import csv

"""
Reads nodes file (patents.txt) and edge file (citations.txt) and convert patent IDs to integers.
This is required for the snap package to work.
"""

def patentID2nodeID(ptID):
    if ptID == "NULL": return 0
    letters2digits = {"" : "1", "D": "2", "H" : "3", "PP" : "4", "RE": "5", "T" : "6"}
    digits = ""
    letters = ""
    for s in ptID:
        if s.isdigit():
            if len(letters)==0 : return int(ptID)
            digits += s
        else:
            letters += s
    if letters2digits.has_key(letters):
        return int(letters2digits[letters] + digits)
    else:
        print ptID
        return "error"


def nodeID2patentID(nID):
    if nID == 0 : return "NULL"
    digits2letters = {"1" : "", "2": "D", "3" : "H", "4" : "PP", "5": "RE", "6": "T"}
    nID = str(nID)
    if len(nID) ==0 : return str(nID)
    return digits2letters[nID[0]] + nID[1:]

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','..'))
input_dir = os.path.join(project_dir, 'data', 'raw')
output_dir = os.path.join(project_dir, 'data', 'processed','patent_ID_to_int')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Reading the files
print("Loading the data")
VERT_FILE_PATH = os.path.join(input_dir, 'patents.txt')
EDGE_FILE_PATH = os.path.join(input_dir, 'citations.txt')

VERT_OUT_FILE_PATH = os.path.join(output_dir, 'patents.txt')
EDGE_OUT_FILE_PATH = os.path.join(output_dir, 'citations.txt')

LIMIT_NUM_ROWS = float("inf") #float("inf") #


print("Converting vertices")
with open(VERT_FILE_PATH, mode='r') as ver_patent_ID, open(VERT_OUT_FILE_PATH, 'wb') as ver_int_ID:
    next(ver_patent_ID)
    csv_writer = csv.writer(ver_int_ID, delimiter=' ')
    row_counter = 0
    for line in ver_patent_ID:
        if row_counter % 100000 == 0 : print(row_counter)
        row_counter +=1
        patentId = patentID2nodeID(line.strip().split()[0])
        csv_writer.writerow([patentId])

        if row_counter >= LIMIT_NUM_ROWS:
            break

print("reading edges")
with open(EDGE_FILE_PATH,  mode='r') as edge_patent_ID, open(EDGE_OUT_FILE_PATH, 'wb') as vf_int_ID:
    next(edge_patent_ID)
    csv_writer = csv.writer(vf_int_ID, delimiter=' ')
    row_counter = 0
    for edgeRow in edge_patent_ID:
        if row_counter % 100000 == 0 : print(row_counter)
        row_counter +=1
        edge = edgeRow.split()
        p0 = patentID2nodeID(edge[0])
        p1 = patentID2nodeID(edge[1])
        csv_writer.writerow([p0,p1])

        if row_counter >= LIMIT_NUM_ROWS:
            break
