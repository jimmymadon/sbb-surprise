class Stop:
    def __init__(self, name, date, time):
        self.name = name
        self.date = date
        self.time = time


class TripInfo:
    def __init__(self, trip_id, destination, origin, price, product_id, description):
        self.tripId = trip_id
        self.destination = destination
        self.origin = origin
        self.price = price
        self.productId = product_id
        self.destination = destination
