import matplotlib as mpl
mpl.use('TkAgg')
from booksoup import BookSoup
import numpy as np
import matplotlib.pyplot as plt
import sys

# Enter the path to the top level of your facebook data folder below.
me = BookSoup(sys.argv[2])

# Enter the name of the conversation or the numerical ID below.
contact = me.load_conversation(sys.argv[1], sys.argv[3])

times = contact.interaction_freq()

objects = sorted(times.keys(), key=contact.get24HourTime)
y_pos = np.arange(len(objects))
vals = [times[t] for t in objects]

plt.bar(y_pos, vals, align='center', alpha=0.5)
plt.xticks(y_pos, objects, fontsize=8, rotation=90)
plt.ylabel('Frequency')
plt.title('Interaction Frequency with ' + contact.name)

plt.show()
