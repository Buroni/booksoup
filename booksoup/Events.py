"""Events.py: stores three lists of Event objects depending on whether
user marked as attending, maybe, declined or didn't reply."""

class Events:
    def __init__(self, attending=[], maybe=[], declined=[], no_reply=[]):
        self.attending = attending
        self.maybe = maybe
        self.declined = declined
        self.no_reply = no_reply