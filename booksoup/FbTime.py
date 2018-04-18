"""FbTime.py: Contains functions used for generating empty timeline/frequency
dictionaries, and building them from conversation data"""

import calendar
from calendar import monthrange


class FbTime:
    def __init__(self, span_meta):
        # Span tags with "meta" class contain a timestamp of when each message was sent.
        self.span_meta = span_meta

    # Returns a dict where each key is a time on the hour and each value is the number of messages sent
    # at that time over the history of the conversation.
    def interaction_freq(self):
        times = self.generate_time_dict()

        for date_str in self.span_meta:
            time = date_str.split("at ")[1][:5]
            hour = time.split(":")[0]
            times[hour+":00"] += 1
        return times

    # Returns a dict where each key is a date and each value is the number of
    # messages sent at that date.
    def interaction_timeline(self, name, messages):
        dates = self.generate_date_dict()
        for message in messages:
            if message.name == name:
                dates[message.date] += 1
        return dates

    # Creates a dictionary of times on the hour where each value is 0.
    def generate_time_dict(self):
        times = {}
        for h in range(0,24):
            time = self.__pad(h) + ":" + "00"
            times[time] = 0
        return times

    # Creates a dictionary of dates where each value is 0.
    def generate_date_dict(self, interval="month"):
        dates = {}
        min_date_arr = [int(i) for i in self.span_meta_to_date(self.span_meta[-1], interval).split("-")]
        max_date_arr = [int(i) for i in self.span_meta_to_date(self.span_meta[0], interval).split("-")]
        for y in range(min_date_arr[0], max_date_arr[0]+1):
            if y == max_date_arr[0]:
                end_month = max_date_arr[1]
            else:
                end_month = 12
            if y == min_date_arr[0]:
                start_month = min_date_arr[1]
            else:
                start_month = 1
            for m in range(start_month, end_month+1):
                if interval == "month":
                    dates[str(y)+"-"+self.__pad(m)] = 0
                    continue
                if m == max_date_arr[1] and y == max_date_arr[0]:
                    end_day = max_date_arr[2]
                else:
                    end_day = monthrange(max_date_arr[0], max_date_arr[1])[1]
                if m == min_date_arr[1] and y == min_date_arr[0]:
                    start_day = min_date_arr[2]
                else:
                    start_day = 1
                for d in range(start_day, end_day+1):
                    dates[str(y)+"-"+self.__pad(m)+"-"+self.__pad(d)] = 0
        return dates

    def __pad(self, val):
        if int(val) < 10:
            return "0"+str(val)
        return str(val)

    # Converts timestamp in <span class="meta">...</span> to YYYY-MM[-DD] format.
    def span_meta_to_date(self, span_str, interval="month"):
        # Remove all occurences of commas except the first one
        if span_str.count(",") == 2:
            span_str = ''.join(span_str.rsplit(',', 1))

        date_arr = span_str.split(", ")[1].split(" ")[:3]
        date_str = date_arr[2]+"-"+self.__pad(list(calendar.month_name).index(date_arr[1]))
        if interval == "day":
            date_str += "-"+self.__pad(date_arr[0])
        return date_str
