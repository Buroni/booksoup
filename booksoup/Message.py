"""Message.py: stores a facebook message as a python object."""


class Message:
    def __init__(self, name, date, timestamp, content):
        self.name = name
        self.date = date
        self.content = content
        self.timestamp = timestamp
