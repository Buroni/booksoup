# -*- coding: UTF-8 -*-

from Conversation import Conversation
from bs4 import BeautifulSoup
import os
import re


class BookSoup:
    def __init__(self, path):
        self.__path = path
        self.conversations = {}
        with open(os.path.join(path,"index.htm"), "r") as f:
            self.__soup = BeautifulSoup(f.read(), "html.parser")
            self.name = self.__soup.find("h1").text

    def load_all_conversations(self, interval="month"):
        for filename in os.listdir(os.path.join(self.__path, "messages")):
            if filename.endswith(".html"):
                contact = Conversation(os.path.join(self.__path, "messages", filename), interval=interval)
                self.conversations[contact.name] = contact

    def load_conversation(self, search_name, interval="month"):
        if isinstance(search_name, int):
            contact = Conversation(os.path.join(self.__path, "messages", str(search_name)+".html"), interval=interval)
            self.conversations[contact.name] = contact
            return contact

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

