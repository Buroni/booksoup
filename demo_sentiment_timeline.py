import matplotlib as mpl
mpl.use('TkAgg')
from booksoup import fbme
import numpy as np
import matplotlib.pyplot as plt

times = []
objects = []
vals = []

me = fbme("facebook-data")

conversation = me.load_conversation(125)

for participant in conversation.participants:
    timeline = conversation.sentiment_timeline(participant)
    sorted_keys = sorted(timeline.keys())
    times.append(timeline)
    objects.append(sorted_keys)
    vals.append([timeline[t] for t in sorted_keys])

y_pos = np.arange(len(objects[0]))

for i,v in enumerate(vals):
    plt.plot(y_pos, v, alpha=0.5, label=conversation.participants[i])

plt.xticks(y_pos, objects[0])
plt.ylabel('Average Sentiment')
plt.title('Sentiment over time with ' + conversation.name)
plt.xticks(fontsize=8, rotation=90)
plt.legend()
plt.show()

