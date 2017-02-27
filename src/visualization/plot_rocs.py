import pickle
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams.update({'xtick.labelsize' : 18})
rcParams.update({'ytick.labelsize' : 18})

fpr_graph, tpr_graph = pickle.load(open('/cs/ai/smdyshel/needleProj/data/processed/dendograms/tpr_fprgraph.pickle', 'rb'))
fpr_tf, tpr_tf = pickle.load(open('/cs/ai/smdyshel/needleProj/data/processed/dendograms/tpr_fprtfidf.pickle', 'rb'))
fpr_both, tpr_both = pickle.load(open('/cs/ai/smdyshel/needleProj/data/processed/dendograms/tpr_fprnew.pickle', 'rb'))

fig, ax = plt.subplots()
x = np.linspace(0,1,50)
ax.plot(fpr_tf, tpr_tf, 'b', label = 'text features', linewidth=2)
ax.plot(fpr_both, tpr_both, 'r', label = 'graph features + both features', linewidth=2)

ax.plot(x,x,'k--')
ax.legend(bbox_to_anchor=(0., 1.), loc=2, )

plt.savefig('ROCs.png')
plt.show()

