from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import requests
# from sklearn.externals import joblib

flask_app = Flask(__name__)
app = Api(app = flask_app,
          version = "1.0",
          title = "SBB Surprise App",
          description = "WIP")

name_space = app.namespace('prediction', description='Prediction APIs')

# model = app.model('Prediction params',
# 				  {'textField1': fields.String(required = True,
# 				  							   description="Text Field 1",
#     					  				 	   help="Text Field 1 cannot be blank"),
# 				  'textField2': fields.String(required = True,
# 				  							   description="Text Field 2",
#     					  				 	   help="Text Field 2 cannot be blank"),
# 				  'select1': fields.Integer(required = True,
# 				  							description="Select 1",
#     					  				 	help="Select 1 cannot be blank"),
# 				  'select2': fields.Integer(required = True,
# 				  							description="Select 2",
#     					  				 	help="Select 2 cannot be blank"),
# 				  'select3': fields.Integer(required = True,
# 				  							description="Select 3",
#     					  				 	help="Select 3 cannot be blank")})

# classifier = joblib.load('classifier.joblib')

@name_space.route("/")
class MainClass(Resource):

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    # @app.expect(model)
    def get(self):
        try:
#             formData = request.json
#             data = [val for val in formData.values()]
            r = requests.get("https://b2p.app.sbb.ch/api/trips?arrivalDeparture=ED&date=2019-11-27&destinationId=8503103&originId=8507000&time=10%3A22&trainType=IR%3BICE%2FTGV%2FRJ%2CEC%2FIC",
                headers={"Accept-Language": "en",
                    "X-Contract-Id": "HAC222P",
                    "X-Conversation-Id": "cafebabe-0815-4711-1234-ffffdeadbeef"})

            response = jsonify({
                "statusCode": 200,
                "status": "Prediction made",
                "result": r.json()
                })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as error:
            return jsonify({
                "statusCode": 500,
                "status": "Error",
                "error": str(error)
            })