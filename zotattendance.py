from flask import Flask, jsonify, send_from_directory, request
import requests
import xml.etree.ElementTree as ET
from user import get_user_record

app = Flask(__name__)

@app.route("/")
def home():
    '''Send index.html when users entered the root URL.'''
    return send_from_directory("static", "index.html")

@app.route("/assets/<static_file>")
def assets(static_file):
    '''Send other static files like images under the assets/ directory.'''
    return send_from_directory("static/assets", static_file)


@app.route("/api/login", methods=["GET"])
def login():
    '''return path after SSO Login validates UCI cookies and gets user details'''
    webauth_cookie = request.cookies.get("ucinetid_auth")
    try:
        user_details = get_user_details(webauth_cookie)
    except Exception as e:
        return "login Failed"

    user_record = get_user_record(user_details)

    return user_record


def get_user_details(webauth_cookie: str)->dict:
    '''Gets User Details from webauth_cookie'''
    url = "https://login.uci.edu/ucinetid/webauth_check?ucinetid_auth="+webauth_cookie+"&return_xml=true"
    r = requests.get(url)
    if r.status_code != 200:
        raise(Exception("Login Validation Failed"))

    root = ET.fromstring(r.text)
    user_details = {}
    for child in root:
        user_details[child.tag] = child.text

    return user_details

if __name__ == "__main__":
    app.run()
