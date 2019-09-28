from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import requests
from db_requests import get_id_by_location, select_random_cities
from flask_cors import CORS, cross_origin
import json


CLIENT_ID = "22ebc2be"
CLIENT_SECRET = "2c820784f3e28837959abc43120989ca"
CONTRACT_ID = "HAC222P"


flask_app = Flask(__name__)
CORS(flask_app, support_credentials=True)
app = Api(app = flask_app,
          version = "1.0",
          title = "SBB Surprise App",
          description = "WIP")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params',
                  {'startingLocation': fields.String(required = True,
                                               description="From",
                                               help="Text Field 1 cannot be blank")})


@name_space.route("/")
# @cross_origin(supports_credentials=True)

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
            date = "2019-11-27"
            time = "10%3A22"
            train_type = "IR%3BICE%2FTGV%2FRJ%2CEC%2FIC"

            destinationIds = select_random_cities(5)
            data_json = json.loads(request.data.decode('utf8'))
            originId = get_id_by_location(data_json['startingLocation'])

            auth = requests.post("https://sso-int.sbb.ch/auth/realms/SBB_Public/protocol/openid-connect/token",
                                # headers={'Access-Control-Allow-Origin', '*'},
                                data={"grant_type": "client_credentials",
                                         "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
                                )
            print(destinationIds)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAA")
            request_results = [requests.get(
                f"https://b2p-int.api.sbb.ch/api/trips?arrivalDeparture=ED&date={date}&destinationId={destinationId}&" +
                f"originId={originId}&time={time}&trainType={train_type}",
                headers={"Accept-Language": "en",
                    "X-Contract-Id": CONTRACT_ID,
                    "X-Conversation-Id": "cafebabe-0815-4711-1234-ffffdeadbeef",
                    "Authorization": ("Bearer " + auth.json()["access_token"]),
                    'Access-Control-Allow-Origin': '*'
                    })
                for destinationId in destinationIds]
            print("FUUUUUCK")
            print(request_results[0].text)
            response = jsonify({
                "statusCode": 200,
                "status": "Prediction made",
                "result": " ".join([r.json()[0]["segments"][0]["destination"]["name"] for r in request_results])
                })
            # response.headers.add('Access-Control-Allow-Origin', '*')
            print("urra")
            print(response)
            return response
        except Exception as error:
            print("porcodio")
            print(error)
            return jsonify({
                "statusCode": 500,
                "status": "Error",
                "error": str(error)
            })

