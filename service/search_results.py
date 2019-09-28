import datetime

class Stop:
    def __init__(self, json_response):
        self.name = json_response["name"]
        self.date = json_response["date"]
        self.time = json_response["time"]


class TripInfo:
    def __init__(self, json_response, json_details):
        self.origin_stop = Stop(json_response["segments"][0]["origin"])
        self.destination_stop = Stop(json_response["segments"][0]["destination"])
        self.tripId = json_response["tripId"]
        self.price = int(json_details["price"])
        self.superSaver = json_details["superSaver"]


def add_to_time(time, mins):
    ans = datetime.datetime.strptime(time, "%H:%M") + datetime.timedelta(minutes=30)
    return ans.strftime("%H:%M")

