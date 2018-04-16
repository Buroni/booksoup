class Events:
    def __init__(self, attending=[], maybe=[], declined=[], no_reply=[]):
        self.attending = attending
        self.maybe = maybe
        self.declined = declined
        self.no_reply = no_reply