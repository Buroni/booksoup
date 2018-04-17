import matplotlib as mpl
mpl.use('TkAgg')
from booksoup import BookSoup
import numpy as np
import matplotlib.pyplot as plt

times = []
objects = []
vals = []

# Enter the path to the top level of your facebook data folder below.
me = BookSoup("facebook-data")

# Enter the name of the conversation or the numerical ID below.
conversation = me.load_conversation(108)

for participant in conversation.participants:
    timeline = conversation.interaction_timeline(participant)
    sorted_keys = sorted(timeline.keys())
    times.append(timeline)
    objects.append(sorted_keys)
    vals.append([timeline[t] for t in sorted_keys])

y_pos = np.arange(len(objects[0]))

for i,v in enumerate(vals):
    plt.plot(y_pos, v, alpha=0.5, label=conversation.participants[i])

plt.xticks(y_pos, objects[0])
plt.ylabel('Message count')
plt.title('Messages over time with ' + conversation.name)
plt.xticks(fontsize=8, rotation=90)
plt.legend()
plt.show()

