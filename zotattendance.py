import requests
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, request, send_from_directory, session
from time import asctime
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'32f87d601a8fb7d44a86f3549c2e62858a4ac74f48b59edeec9449fed58becf0'    # Replace this key


@app.route("/")
def show_index_or_home():
    '''Send index.html or home.html depending on whether users logged in or not.'''
    if 'logged_in' not in session:
        return send_from_directory("static", "index.html")
    else:
        return send_from_directory("static", "home.html")

@app.route("/assets/<static_file>")
def assets(static_file: str):
    '''Send other static files like images under the assets/ directory.'''
    return send_from_directory("static/assets", static_file)

@app.route("/api/login")
def login():
    '''Return path after SSO Login validates UCI cookies and gets user details.'''
    try:
        user_details = get_user_details(request.cookies.get("ucinetid_auth"))
        session['logged_in'] = True

        mongo_client = MongoClient('localhost', 27017)
        sso_collection = mongo_client['sso_db']['user_details']
        sso_collection.insert_one(user_details)

        return send_from_directory("static", "home.html")
    except Exception as e:
        app.logger.error(f'{asctime()} repr(error)')
        return send_from_directory("static", "error.html")

def get_user_details(webauth_cookie: str) -> dict:
    '''Gets User Details from webauth_cookie'''
    url = "https://login.uci.edu/ucinetid/webauth_check?ucinetid_auth=" + webauth_cookie + "&return_xml=true"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Login Validation Failed")

    root = ET.fromstring(r.text)
    user_details = {}
    for child in root:
        user_details[child.tag] = child.text

    return user_details

if __name__ == "__main__":
    app.run()
