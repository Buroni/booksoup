
class Event:
    def __init__(self, title, timestamp, location, description):
        self.title = title
        self.timestamp = timestamp
        self.location = location
        self.latlon = self.__latlon(location)
        self.description = description

    def __latlon(self, location):
        if not("(Latitude:" in location):
            return None
        lat = float(find_between(location, "(Latitude: ", ","))
        lon = float(find_between(location, "Longitude: ", ")"))
        return [lat, lon]



def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

