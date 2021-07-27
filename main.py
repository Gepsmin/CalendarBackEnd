from flask import Flask, request, Response
import pymongo
import os

USER_NAME = os.getenv('user_name')
USER_PASSWORD = os.getenv('user_password')

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.dbcb9.mongodb.net/first".format(USER_NAME, USER_PASSWORD))
db = client.first
collection = db.calendar


@app.route('/sign_up', methods=["OPTIONS", "POST"])
def sign_up():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = 'access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type'
        res.headers['Content-Type'] = 'application/json'
        value = {
            'options': 'passed'
        }
        return value, 200, res.headers
    elif request.method == "POST":

        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = 'access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type'
        res.headers['Content-Type'] = 'application/json'

        request_data = request.get_json()
        user = collection.find_one({"_id": request_data['user_name']})
        if user:
            value = {
                'user_name': user['_id'],
                'result': 'Already Signed'
            }
            return value, 400, res.headers

        x = collection.insert_one({'_id': request_data['user_name'], 'password': request_data['password']})

        value = {
            'user_name': x.inserted_id,
            'result': 'success'
        }

        return value, 201, res.headers


@app.route('/sign_in/<name>/<password>', methods=["OPTIONS", "GET"])
def sign_in(name, password):
    if request.method == "OPTIONS":
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = 'access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type'
        res.headers['Content-Type'] = 'application/json'
        value = {
            'options': 'passed'
        }
        return value, 200, res.headers
    elif request.method == "GET":
        x = collection.find_one({'_id': name, 'password': password})
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers[
            'Access-Control-Allow-Headers'] = 'access-control-allow-headers,access-control-allow-methods,access-control-allow-origin,content-type'
        res.headers['Content-Type'] = 'application/json'
        if x:
            value = {
                'user_name': x['_id'],
                'result': 'success'
            }

            return value, 200, res.headers

        value = {
            'user_name': name,
            'result': 'failure'
        }
        return value, 400, res.headers


if __name__ == '__main__':
    app.run(debug=True)
