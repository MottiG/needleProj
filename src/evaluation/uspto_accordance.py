import pandas as pd
import numpy
import random
import os
from collections import deque, Counter
import matplotlib.pyplot as plt

SAMPLE = "sample"
project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
unconnected_articles_file = os.path.join(input_dir, 'unconnected_patents.pickle')
topclass_neighbors_file = os.path.join(input_dir, 'topclass_neighbors.pickle')
subclass_neighbors_file = os.path.join(input_dir, 'subclass_neighbors.pickle')


