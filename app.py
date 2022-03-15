from urllib import request
from flask import Flask
from flask import request
from flask import jsonify
from flask import session

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api", methods=['POST','GET'])
def api():
    print(request.method)
    print(request.form)
    print(request.files)
    return jsonify(["a","b","c"])