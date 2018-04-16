from booksoup import BookSoup

me = BookSoup("facebook-data")

events = me.load_all_events()

for event in events.attending:
    print(event.title, event.description, event.location, event.timestamp, event.latlon)