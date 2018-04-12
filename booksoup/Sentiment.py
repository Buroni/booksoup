from textblob import TextBlob


class Sentiment:

    def __init__(self, messages, fbt):
        self.fbt = fbt
        self.messages = messages

    def sentiment_timeline(self, name):
        timeline = self.fbt.generate_date_dict()
        sentiment_counts = self.fbt.generate_date_dict()
        for message in self.messages:
            if message.content is None or message.name != name:
                continue
            blob = TextBlob(message.content)
            timeline[message.date] += blob.sentiment.polarity
            sentiment_counts[message.date] += 1

        for k,v in timeline.iteritems():
            if v == 0:
                continue
            timeline[k] = v/sentiment_counts[k]
        return timeline

    def avg_sentiment(self, name):
        sentiments = []
        for message in self.messages:
            message_text = message.content
            if message_text is None or message.name != name:
                continue
            sentiments.append(TextBlob(message_text).sentiment.polarity)
        return sum(sentiments) / len(sentiments)

