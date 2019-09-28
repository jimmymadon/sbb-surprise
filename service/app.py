from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import requests
from flask_cors import CORS, cross_origin
import json

from db_requests import select_random_cities, get_id_by_location
from search_results import TripInfo, add_to_time, RequestParams, call_for_offer_details, select_results


CLIENT_ID = "22ebc2be"
CLIENT_SECRET = "2c820784f3e28837959abc43120989ca"


flask_app = Flask(__name__)
CORS(flask_app, support_credentials=True)
app = Api(app = flask_app,
          version = "1.0",
          title = "SBB Surprise App",
          description = "WIP")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params',
                  {'startingLocation': fields.String(required=True, description="From",
                                                     help="Text Field 1 cannot be blank"),
                   "dateOfTravel": fields.String(required=True, description="data"),
                   "timeOfTravel": fields.String(required=True, description="time")})


@name_space.route("/")

class MainClass(Resource):

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    @app.expect(model)
    def post(self):
        try:
            destinationIds = select_random_cities(10)
            data_json = json.loads(request.data.decode('utf8'))
            originId = get_id_by_location(data_json['startingLocation'])
            departure_date = data_json['dateOfTravel']
            departure_time = data_json['timeOfTravel']
            search_params = RequestParams(departure_date, destinationIds, originId, departure_time)

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
            if not return_tickets:
                response = jsonify({
                    "statusCode": 200,
                    "status": "NotFound"
                })
            best_ss = sorted(return_tickets)[0]
            forward_ticket, backward_ticket = all_ss_tickets[best_ss]
            response = jsonify({
                "statusCode": 200,
                "status": "SuperSaver",
                "result": forward_ticket.destination_stop.name,
                "from": forward_ticket.origin_stop.name,
                "to": forward_ticket.destination_stop.name,
                "date": departure_date,
                "forward_dep_time": forward_ticket.origin_stop.time,
                "forward_arr_date": forward_ticket.destination_stop.time,
                "backward_dep_time": backward_ticket.origin_stop.time,
                "backward_arr_time": backward_ticket.destination_stop.time,
                "price_forward": forward_ticket.price,
                "price_backward": backward_ticket.price
            })
            #print(response)
            return response
        except Exception as error:
            #print(error)
            return jsonify({
                "statusCode": 500,
                "status": "Error",
                "error": str(error)
            })

