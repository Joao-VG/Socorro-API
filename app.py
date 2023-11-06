from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


print(app.config['SQLALCHEMY_DATABASE_URI'])

class User(db.Model):
    __tablename__ = 'USERS'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthDate = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    phone = db.Column(db.String(14), unique=False, nullable=False)
    CEP = db.Column(db.String(8), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'cpf': self.cpf, 'email': self.email, 'birthDate': self.birthDate, 'phone': self.phone, 'CEP': self.CEP, 'address': self.address}

class Employee(db.Model):
    __tablename__ = 'EMPLOYEES'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('employee', lazy=True))
    role = db.Column(db.String(80), unique=False, nullable=False)
    salary = db.Column(db.Float, unique=False, nullable=False)
    admissionDate = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    resignationDate = db.Column(db.TIMESTAMP, unique=False, nullable=True)
    status = db.Column(db.String(80), unique=False, nullable=False)
    def json(self):
        return {'id': self.id,'role': self.role, 'salary': self.salary, 'admissionDate': self.admissionDate, 'resignationDate': self.resignationDate, 'status': self.status}


class Client(db.Model):
    __tablename__ = 'CLIENTS'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('client', lazy=True))
    clientType = db.Column(db.String(80), unique=False, nullable=False)
    def json(self):
        return {'id': self.id}


class Service(db.Model):
    __tablename__ = 'SERVICES'
    id = db.Column(db.Integer, primary_key=True)
    serviceType = db.Column(db.String(80), unique=False, nullable=False)
    serviceDescription = db.Column(db.String(120), unique=False, nullable=False)
    serviceDate = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('EMPLOYEES.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('CLIENTS.id'), nullable=False)

class Emergency(db.Model):
    __tablename__ = 'EMERGENCIES'
    id = db.Column(db.Integer, primary_key=True)
    emergencyType = db.Column(db.String(80), unique=False, nullable=False)
    emergencyDescription = db.Column(db.String(120), unique=False, nullable=False)
    emergencyDate = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('EMPLOYEES.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('CLIENTS.id'), nullable=False)


db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


# create a user
@app.route('/users', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created'}), 201)
  except e:
    return make_response(jsonify({'message': 'error creating user'}), 500)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting users'}), 500)

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting user'}), 500)

# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating user'}), 500)

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting user'}), 500)