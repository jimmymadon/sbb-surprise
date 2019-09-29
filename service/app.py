from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import requests
from flask_cors import CORS, cross_origin
import json
import pandas as pd

from .db_requests import select_random_cities, get_id_by_location, get_location_by_id
from .search_results import RequestParams, select_results, combine_with_return_tickets


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
                  {'startingLocation': fields.String(required=True, description="from",
                                                     help="Text Field 1 cannot be blank"),
                   "dateOfTravel": fields.String(required=True, description="data"),
                   "timeOfTravel": fields.String(required=True, description="time"),
                   "preferredActivities": fields.String(required=True, description="activities")
                   })


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
            data_json = json.loads(request.data.decode('utf8'))
            originId = get_id_by_location(data_json['startingLocation'])
            departure_date = data_json['dateOfTravel']
            departure_time = data_json['timeOfTravel']
            preferred_activities = ['shopping'] #data_json['preferredActivities']
            preferred_activity = preferred_activities[0]

            auth = requests.post("https://sso-int.sbb.ch/auth/realms/SBB_Public/protocol/openid-connect/token",
                                 data={"grant_type": "client_credentials",
                                       "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
            access_token = auth.json()["access_token"]

            response = jsonify({
                        "statusCode": 200,
                        "status": "NotFound",
                        "result": "NotFound"
                        })
            for _ in range(10):
                destinationIds = select_random_cities(5, f"../stops_{preferred_activity}_df.csv")
                print([get_location_by_id(id) for id in destinationIds])
                search_params = RequestParams(departure_date, destinationIds, originId, departure_time)
                offers_dict = select_results(search_params, access_token)
                return_tickets, all_ss_tickets = combine_with_return_tickets(
                    offers_dict, originId, departure_date, access_token)

                if return_tickets:
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
            return response
        except Exception as error:
            return jsonify({
                "statusCode": 500,
                "status": "Error",
                "error": str(error)
            })

