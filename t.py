from booksoup import BookSoup

me = BookSoup("facebook-data")

# Get a conversation by name
convo = me.load_conversation("Jaki Reid")

# Print participants of the conversation
print(convo.participants)
