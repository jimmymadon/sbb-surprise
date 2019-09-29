import datetime
import requests


CONTRACT_ID = "HAC222P"
CONVERSATION_ID = "cafebabe-0815-4711-1234-ffffdeadbeef"  # make changable
API_LINK = "https://b2p-int.api.sbb.ch/api/"
PASSENGER_DEFAULT_INFO = "paxa;42;half-fare"
DEFAULT_TRAIN_TYPE = "IR%3BICE%2FTGV%2FRJ%2CEC%2FIC"


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


class RequestParams:
    def __init__(self, date, destinationIds, originId, time, train_type=DEFAULT_TRAIN_TYPE):
        self.departure_date = date
        self.destinationIds = destinationIds
        self.originId = originId
        h, min = time.split(':')
        self.time = h + "%3A" + min
        self.train_type = train_type


def call_for_offer_details(trip_info, access_token):
    headers = {"Accept-Language": "en",
               "X-Contract-Id": CONTRACT_ID,
               "X-Conversation-Id": CONVERSATION_ID,
               "Authorization": ("Bearer " + access_token)
               }
    trip_id = trip_info["tripId"]
    result = requests.get(f"{API_LINK}v2/prices?tripIds={trip_id}&passengers={PASSENGER_DEFAULT_INFO}", headers=headers)
    if result.status_code != 200:
        return None
    return result.json()[0]


def select_results(params, access_token):
    headers = {"Accept-Language": "en",
               "X-Contract-Id": CONTRACT_ID,
               "X-Conversation-Id": CONVERSATION_ID,
               "Authorization": ("Bearer " + access_token)
               }

    request_results = [requests.get(
        f"{API_LINK}trips?arrivalDeparture=ED&date={params.departure_date}&" +
        f"destinationId={destinationId}&originId={params.originId}&time={params.time}&trainType={params.train_type}",
        headers=headers) for destinationId in params.destinationIds]

    request_results = [r.json() for r in request_results if r.status_code == 200]
    offers_details = [[call_for_offer_details(offer, access_token) for offer in res] for res in request_results]
    offers = dict([(destinationId, []) for destinationId in params.destinationIds])
    for destinationId, destination_offers, destination_details in zip(params.destinationIds, request_results, offers_details):
        for offer, details in zip(destination_offers, destination_details):
            if details is not None:
                offers[destinationId].append(TripInfo(offer, details))
    return offers


def combine_with_return_tickets(offers_dict, originId, departure_date, access_token):
    return_tickets = []
    back_offers_dict = dict([(destinationId, []) for destinationId in offers_dict.keys()])
    all_ss_tickets = {}
    for destinationId, destination_offers in offers_dict.items():
        for i, offer in enumerate(destination_offers):
            search_params = RequestParams(departure_date, [originId], destinationId,
                                          add_to_time(offer.destination_stop.time, 30))
            back_offers_list = list(select_results(search_params, access_token).values())[0]
            if i == 0:
                back_offers_dict[destinationId].extend(back_offers_list)
            for back_offer in back_offers_list:
                if offer.superSaver or back_offer.superSaver:
                    h, m = back_offer.destination_stop.time.split(":")
                    sort_key = (offer.price + back_offer.price, offer.origin_stop.time, -int(h), -int(m))
                    all_ss_tickets[sort_key] = (offer, back_offer)
                    return_tickets.append(sort_key)
    return return_tickets, all_ss_tickets
