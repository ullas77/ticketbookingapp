from flask_restful import Api, Resource
api=Api(prefix="/api")

user={
    "username":"Ullas",
    "email": "ullas@gmail.com"
}



class User(Resource):
    def get(self):
        return user
    

api.add_resource(User, '/users')
