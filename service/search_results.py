class Stop:
    def __init__(self, name, date, time):
        self.name = name
        self.date = date
        self.time = time


class TripInfo:
    def __init__(self, json_response):
        self.origin_stop = Stop(json_response["segments"][0]["origin"])
        self.destination_stop = Stop(json_response["segments"][0]["destination"])
        self.tripId = json_response["trip_id"]
