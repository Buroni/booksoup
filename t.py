from booksoup import BookSoup

me = BookSoup("facebook-data")

events = me.load_all_events()

# Events are organised into attending, maybe, declined and no_reply:
for event in events.attending:
    print(event.title, event.description, event.location, event.timestamp, event.latlon)