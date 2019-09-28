from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import requests

flask_app = Flask(__name__)
app = Api(app = flask_app,
          version = "1.0",
          title = "SBB Surprise App",
          description = "WIP")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params',
                  {'origin': fields.String(required = True,
                                               description="From",
                                               help="Text Field 1 cannot be blank"),
                  'textField2': fields.String(required = True,
                                               description="Text Field 2",
                                               help="Text Field 2 cannot be blank"),
                  'select1': fields.Integer(required = True,
                                            description="Select 1",
                                            help="Select 1 cannot be blank"),
                  'select2': fields.Integer(required = True,
                                            description="Select 2",
                                            help="Select 2 cannot be blank"),
                  'select3': fields.Integer(required = True,
                                            description="Select 3",
                                            help="Select 3 cannot be blank")})


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
            date = "2019-11-27"
            destinationId = 8503103
            OriginId = 8507000
            time = "10%3A22"
            train_type = "IR%3BICE%2FTGV%2FRJ%2CEC%2FIC"
            r = requests.get(
                f"https://b2p.app.sbb.ch/api/trips?arrivalDeparture=ED&date={date}&destinationId={destinationId}&" +
                f"originId={OriginId}&time={time}&trainType={train_type}",
                headers={"Accept-Language": "en",
                    "X-Contract-Id": "HAC222P",
                    "X-Conversation-Id": "cafebabe-0815-4711-1234-ffffdeadbeef"})

            response = jsonify({
                "statusCode": 200,
                "status": "Prediction made",
                "result": r.json()[0]["segments"][0]["destination"]["name"]
                })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as error:
            return jsonify({
                "statusCode": 500,
                "status": "Error",
                "error": str(error)
            })
