from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///users_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


user_arg = reqparse.RequestParser()
user_arg.add_argument('username', type=str, help="Name of the User", required=True)
user_arg.add_argument('email', type=str, help="Email of the User")
user_arg.add_argument('password', type=str, help="Password of the User")
resource_user = {
    'id': fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
}


class Hello(Resource):
    @marshal_with(resource_user)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    @marshal_with(resource_user)
    def put(self, user_id):
        args = user_arg.parse_args()
        user = User(id=user_id, username=args['username'], email=args["email"], password=args["password"])
        db.session.add(user)
        db.session.commit()
        return user

    # def delete(self, user_id):
    #     user_not_exist(user_id)
    #     del users[user_id]
    #     return 'User deleted successfully', 204


# api.add_resource is used to add resource and other parameter is for the end point.


api.add_resource(Hello, "/abc/<int:user_id>")

if __name__ == '__main__':
    app.run(debug=True)
