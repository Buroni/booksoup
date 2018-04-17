"""BookSoup.py: stores a facebook user as a python object with ability to
analyse events, conversations and participants."""
__author__ = "Jake Reid Browning"
__license__ = "MIT"
__email__ = "jake.reid.browning@gmail.com"

# -*- coding: UTF-8 -*-

from Conversation import Conversation
from Events import Events
from Event import Event
from Event import find_between
from bs4 import BeautifulSoup
import os
import re


class BookSoup:
    def __init__(self, path):
        self.__path = path
        self.conversations = {}
        self.events = Events()
        with open(os.path.join(path,"index.htm"), "r") as f:
            self.__soup = BeautifulSoup(f.read(), "html.parser")
            self.name = self.__soup.find("h1").text

    def load_all_conversations(self, interval="month"):
        for filename in os.listdir(os.path.join(self.__path, "messages")):
            if filename.endswith(".html"):
                contact = Conversation(os.path.join(self.__path, "messages", filename), interval=interval)
                self.conversations[contact.name] = contact

    def load_conversation(self, search_name, interval="month"):
        # If search_name is an integer, simply get the HTML file whose name is that integer.
        if isinstance(search_name, int):
            contact = Conversation(os.path.join(self.__path, "messages", str(search_name)+".html"), interval=interval)
            self.conversations[contact.name] = contact
            return contact

        # If the search name is a string, get the list of links leading to conversations,
        # find the relative link and load the conversation using the link path.
        with open(os.path.join(self.__path,"html", "messages.htm"), "r") as infile:
            soup = BeautifulSoup(infile.read(), "html.parser")
            convo_links = soup.find_all("a", {"href": re.compile('.*messages.*')})
            for link in convo_links:
                if link.text != search_name:
                    continue
                contact = Conversation(os.path.join(self.__path, link["href"]))
                self.conversations[contact.name] = contact
                return contact
        return None

    def load_all_events(self):
        with open(os.path.join(self.__path,"html","events.htm"), "r") as f:
            # Replace any number of chained <br />...<br /> tags with a single [BREAK] for easier splitting later.
            f_read = re.sub('(\<br \/\>)+', '[BREAK]', f.read())
            attending_soup = BeautifulSoup(find_between(f_read, "<h3>Attending</h3>", "<h3>Maybe</h3>"), "html.parser")
            maybe_soup = BeautifulSoup(find_between(f_read, "<h3>Maybe</h3>", "<h3>Declined</h3>"), "html.parser")
            declined_soup = BeautifulSoup(find_between(f_read, "<h3>Declined</h3>", "<h3>No reply</h3>"), "html.parser")
            no_reply_soup = BeautifulSoup(f_read.split("<h3>No reply</h3>")[1], "html.parser")

            self.__events_from_li(attending_soup, "attending")
            self.__events_from_li(maybe_soup, "maybe")
            self.__events_from_li(declined_soup, "declined")
            self.__events_from_li(no_reply_soup, "no_reply")
        return self.events

    # Each event is stored by FB as an <li> element where different types of info are separated by line breaks.
    # Split the info on line breaks and append the appropriate list in the events object.
    def __events_from_li(self, soup, attending_type):
        for event_li in soup.find_all("li"):
            event_split = event_li.text.split("[BREAK]")
            if len(event_split) < 4:
                new_event = Event(event_split[0], event_split[1], "", event_split[2])
            else:
                new_event = Event(event_split[0], event_split[1], event_split[2], event_split[3])
            if attending_type == "attending":
                self.events.attending.append(new_event)
            elif attending_type == "maybe":
                self.events.maybe.append(new_event)
            elif attending_type == "declined":
                self.events.declined.append(new_event)
            elif attending_type == "no_reply":
                self.events.no_reply.append(new_event)