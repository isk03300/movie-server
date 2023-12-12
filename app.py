from flask import Flask
from flask_restful import Api
from resources.user import MovieUserResource

app = Flask(__name__)
api = Api(app)

api.add_resource(MovieUserResource  ,  '/user')

if __name__ == '__main__' :
    app.run()