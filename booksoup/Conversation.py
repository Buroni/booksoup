"""Conversation.py: stores a facebook conversation as a python object,
and performs some basic analysis on interaction frequency and sentiment."""

from bs4 import BeautifulSoup
from FbTime import FbTime
from Sentiment import Sentiment
from Message import Message


class Conversation:
    def __init__(self, path, interval="month"):
        with open(path, 'r') as f:
            self.__soup = BeautifulSoup(f.read(), "html.parser")
            self.messages = []
            self.name = self.__soup.find("title").text.replace("Conversation with ", "")
            message_headers = self.__soup.find_all("div", class_="message_header")
            self.__span_meta = [m.find("span", class_="meta").text for m in message_headers]
            self.__fbt = FbTime(self.__span_meta)

            for m in self.__soup.find_all("div", class_="message"):
                span = m.find("span", class_="meta")
                self.messages.append(Message(m.find("span", class_="user").text, self.__fbt.span_meta_to_date(span.text, interval), span.text, m.next_sibling.text))

            self.__sent = Sentiment(self.messages, self.__fbt)
            self.participants = self.__scrape_participants()

    def interaction_freq(self):
        return self.__fbt.interaction_freq()

    def interaction_timeline(self, name):
        return self.__fbt.interaction_timeline(name, self.messages)

    def sentiment_timeline(self, name):
        return self.__sent.sentiment_timeline(name)

    def avg_sentiment(self, name):
        return self.__sent.avg_sentiment(name)

    # Returns a list of participants in the conversation.
    def __scrape_participants(self):
        users = []
        for user_span in self.__soup.find_all("span", "user"):
            user_name = user_span.text
            if user_name not in users:
                users.append(user_name)
        return users


