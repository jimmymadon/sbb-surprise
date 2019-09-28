import requests
import argparse

from db_requests import select_random_cities, get_id_by_location
from search_results import TripInfo


CLIENT_ID = "22ebc2be"
CLIENT_SECRET = "2c820784f3e28837959abc43120989ca"
CONTRACT_ID = "HAC222P"
CONVERSATION_ID = "cafebabe-0815-4711-1234-ffffdeadbeef"  # make changeble


def call_for_offer_details(trip_info, access_token):
    headers = {"Accept-Language": "en",
               "X-Contract-Id": CONTRACT_ID,
               "X-Conversation-Id": CONVERSATION_ID,
               "Authorization": ("Bearer " + access_token)
               }
    


def select_results(params, access_token):
    headers = {"Accept-Language": "en",
               "X-Contract-Id": CONTRACT_ID,
               "X-Conversation-Id": CONVERSATION_ID,
               "Authorization": ("Bearer " + access_token)
               }

    request_results = [[requests.get(
        f"https://b2p-int.api.sbb.ch/api/trips?arrivalDeparture=ED&date={params.departure_date}&" +
        f"destinationId={destinationId}&originId={originId}&time={params.time}&trainType={params.train_type}",
        headers=headers)
        for destinationId in params.destinationIds] for originId in params.originIds]
    request_results = [i for j in request_results for i in j]

    print([r for r in request_results if r.status_code < 400])
    print([r.json()[0]["segments"][0]["destination"]["name"] for r in request_results if r.status_code == 200])

    offers_details = [call_for_offer_details(res, access_token) for res in request_results]
    offers = [TripInfo(res, details) for res, details in zip(request_results, offers_details)]
    return offers


class RequestParams:
    def __init__(self, date, destinationIds, originIds, time, train_type):
        self.departure_date = date
        self.destinationIds = destinationIds
        self.originIds = originIds
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
    destinationIds = select_random_cities(5)
    originIds = get_id_by_location(start_location)
    search_params = RequestParams(departure_date, destinationIds, originIds, args.time, args.train_type)

    auth = requests.post("https://sso-int.sbb.ch/auth/realms/SBB_Public/protocol/openid-connect/token",
                        data={"grant_type": "client_credentials",
                              "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    access_token = auth.json()["access_token"]

    offers_list = select_results(destinationIds, access_token)
    return_offers_list = select_results(destinationIds, access_token)
    for offer in offers_list:
        print(offer.origin_stop)



if __name__ == '__main__':
    main()
