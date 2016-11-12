from flask import Flask
from flask_restful import Resource, Api
from handler import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Handler, '/<string:short_url>', '/')

if __name__ == '__main__':
    app.run(debug=True)

