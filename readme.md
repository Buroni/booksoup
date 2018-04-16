## Booksoup

Booksoup allows you to analyse and traverse your [downloaded facebook data](https://www.facebook.com/help/212802592074644?in_context), 
including features such as sentiment analysis and message frequency analysis over time.

Booksoup requires [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [TextBlob](http://textblob.readthedocs.io/en/dev/), and requires [matplotlib](https://matplotlib.org/) to run the demo graphs.

## Usage

Initialise a new instance of the `BookSoup` class, passing in the top-level path of your facebook data folder as an argument.


### Basic usage

```python
from booksoup import BookSoup

me = BookSoup("facebook-data")

# Get a conversation by name
convo = me.load_conversation("Jane Doe")

# Print participants of the conversation
print(convo.participants)

# Print messages in the conversation
for message in convo.messages:
    print(message.date, message.timestamp, message.name, message.content)
```

### Interaction frequency
It's possible to see how often messages are sent in a specific conversation at each hour of the day using `interaction_freq`,
which returns a dict with each key being an hour in the day and the corresponding value being the number of messages sent at that time.
```python
me = BookSoup("facebook-data")
convo = me.load_conversation("John Smith")

times = convo.interaction_freq()
```

Using the `demo_interaction_frequency.py` code, this can be visualised:

![Interaction frequency example](https://i.imgur.com/cALmzb5.png)

### Interaction timeline

It's also possible to view how many times a specific person within a conversation sent messages from the beginning to the last point
of the conversation using `interaction_timeline(name)`. The following example shows how often I sent messages within a group conversation.

```python
me = BookSoup("facebook-data")
convo = me.load_conversation("Lewis, Andrew, Michelle and 4 others")

times = convo.interaction_timeline(me.name)
```

Using the `demo_interaction_timeline.py` code, I can visualise in one graph how often everyone in the conversation spoke by building a separate
timeline for each person.

![Interaction timeline example](https://i.imgur.com/7BP4GNi.png)

### Sentiment

Booksoup can also perform [sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis). Average sentiment for a user in a specific conversation can be calculated using
`Conversation.avg_sentiment(name)`, or a timeline of average sentiment can also be built using `Conversation.sentiment_timeline`.

```python
convo = me.load_conversation("David Grocer")

# Print the average sentiment of David Grocer in the conversation
print(convo.avg_sentiment("David Grocer"))

# Print the timeline dictionary of my average sentiment in the conversation
print(convo.sentiment_timeline(me.name))

```

### Loading a conversation
A conversation can either be loaded using either the title of the conversation (as in all the previous examples) or the numerical
ID of the conversation (the filename of the conversation's html file).

```python
convo = me.load_conversation(40)
```

### Specifying interval duration

In all of the timeline examples, the interval can be specified as either `month` or `day`, with the default being `month`. To switch to daily intervals
for timeline operations, set the `interval` argument, e.g

```python
convo = me.load_conversation("David Grocer", interval="day")
```

### Events

Booksoup can extract and categorise event information. This includes title, description, location, timestamp and a 2-element array
containing the latitude and longitude of the event if available.

```python
me = BookSoup("facebook-data")

events = me.load_all_events()

# Events are organised into attending, maybe, declined and no_reply:
for event in events.attending:
    print(event.title, event.description, event.location, event.timestamp, event.latlon)
```