import matplotlib as mpl
mpl.use('TkAgg')
from booksoup import BookSoup
import numpy as np
import matplotlib.pyplot as plt
import sys

# Enter the path to the top level of your facebook data folder below.
me = BookSoup(sys.argv[2])

# Enter the name of the conversation or the numerical ID below.
contact = me.load_conversation(sys.argv[1])

times = contact.interaction_freq()
def get24HourTime(elem):
    amOrPm = elem.split(":")[1][2:4]
    hour = int(elem.split(":")[0])
    if amOrPm == "am":
        if hour == 12:
            return hour+12
        return hour
    else:
        if hour == 12:
            return hour
        return hour+12


objects = sorted(times.keys(), key=get24HourTime)
print objects
y_pos = np.arange(len(objects))
vals = [times[t] for t in objects]

plt.bar(y_pos, vals, align='center', alpha=0.5)
plt.xticks(y_pos, objects, fontsize=8, rotation=90)
plt.ylabel('Frequency')
plt.title('Interaction Frequency with ' + contact.name)

plt.show()
