from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# initialize
app = Flask(__name__)
# setting up base directory
app.config['SECRET_KEY'] = 'sdffr43rgvfe566677nff34555'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False, index=True)
    email = db.Column(db.String, unique=True, nullable=False, index=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


# Make a Schema

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


# initialize a schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/users', methods=['POST'])
def adduser():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)


# Get all the Users

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)


# Gets a specific User
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Updates a specific User
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user.username = username
    user.email = email
    user.password = password
    db.session.commit()
    return user_schema.jsonify(user)


# Deletes a Specific User
@app.route('/users/<id>', methods=['DELETE'])
def del_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


# run server
if __name__ == '__main__':
    app.run(debug=True)
