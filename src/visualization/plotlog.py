from collections import Counter
import matplotlib.pyplot as plt


def plotlog(data):
    frequencHist = Counter(data)
    plt.loglog(list(frequencHist.keys()), list(frequencHist.values()), 'ro')
    plt.xlabel('log degree')
    plt.ylabel('log frequency')
    figureName = 'citation graph degree distribution'
    plt.title(figureName)
    plt.show()
    plt.savefig(figureName + '.png')
    plt.clf()


