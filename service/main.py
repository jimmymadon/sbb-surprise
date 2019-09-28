import requests
import argparse

from db_requests import select_random_cities, get_id_by_location
from search_results import TripInfo, add_to_time
#from app import call_for_offer_details, select_results

CLIENT_ID = "22ebc2be"
CLIENT_SECRET = "2c820784f3e28837959abc43120989ca"
CONTRACT_ID = "HAC222P"
CONVERSATION_ID = "cafebabe-0815-4711-1234-ffffdeadbeef"  # make changable
API_LINK = "https://b2p-int.api.sbb.ch/api/"
PASSENGER_DEFAULT_INFO = "paxa;42;half-fare"


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

    #print([r for r in request_results if r.status_code < 400])
    print([r.json()[0]["segments"][0]["destination"]["name"] for r in request_results if r.status_code == 200])

    request_results = [r.json() for r in request_results if r.status_code == 200]
    offers_details = [[call_for_offer_details(offer, access_token) for offer in res] for res in request_results]
    offers = dict([(destinationId, []) for destinationId in params.destinationIds])
    for destinationId, destination_offers, destination_details in zip(params.destinationIds, request_results, offers_details):
        for offer, details in zip(destination_offers, destination_details):
            if details is not None:
                offers[destinationId].append(TripInfo(offer, details))
    return offers


class RequestParams:
    def __init__(self, date, destinationIds, originId, time, train_type):
        self.departure_date = date
        self.destinationIds = destinationIds
        self.originId = originId
        h, min = time.split(':')
        self.time = h + "%3A" + min
        self.train_type = train_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--starting_location', type=str, required=True)
    parser.add_argument('--date', type=str, required=True)
    parser.add_argument('--time', type=str, default="10:00")
    parser.add_argument('--train_type', type=str, default="IR%3BICE%2FTGV%2FRJ%2CEC%2FIC")

    args = parser.parse_args()

    start_location = args.starting_location
    departure_date = args.date
    destinationIds = select_random_cities(10)
    originId = get_id_by_location(start_location)
    destinationIds = [8503000, 8505000]
    originId = 8502204
    search_params = RequestParams(departure_date, destinationIds, originId, args.time, args.train_type)

    auth = requests.post("https://sso-int.sbb.ch/auth/realms/SBB_Public/protocol/openid-connect/token",
                        data={"grant_type": "client_credentials",
                              "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    access_token = auth.json()["access_token"]

    offers_dict = select_results(search_params, access_token)

    return_tickets = []
    back_offers_dict = dict([(destinationId, []) for destinationId in destinationIds])
    all_ss_tickets = {}
    for destinationId, destination_offers in offers_dict.items():
        for i, offer in enumerate(destination_offers):
            search_params = RequestParams(departure_date, [originId], destinationId,
                                          add_to_time(offer.destination_stop.time, 30), args.train_type)
            back_offers_list = list(select_results(search_params, access_token).values())[0]
            if i == 0:
                back_offers_dict[destinationId].extend(back_offers_list)
            for back_offer in back_offers_list:
                if offer.superSaver or back_offer.superSaver:
                    h, m = back_offer.destination_stop.time.split(":")
                    sort_key = (offer.price + back_offer.price, offer.origin_stop.time, -int(h), -int(m))
                    all_ss_tickets[sort_key] = (offer, back_offer)
                    return_tickets.append(sort_key)
    # for price, offer, o in return_tickets:
    #     print(price)
    #     print(offer.origin_stop.name, offer.origin_stop.time, offer.destination_stop.name, offer.destination_stop.time)
    #     print(o.origin_stop.name, o.origin_stop.time, o.destination_stop.name, o.destination_stop.time)
    #     print('=================')
    best_ss = sorted(return_tickets)[0]
    print(best_ss)
    print(all_ss_tickets[best_ss])



if __name__ == '__main__':
    main()
