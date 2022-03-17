import requests
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, redirect, request, send_from_directory, session, url_for
from time import asctime
from user import get_user_record


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
        session['user_record'] = get_user_record(user_details)
        return redirect(url_for("/"), code=200)
    except Exception as e:
        app.logger.error(f'{asctime()} {repr(e)}')
        return send_from_directory("static", "error.html")

@app.route("/api/courses")
def courses():
    try:
        return jsonify(session['user_record']['courses'])
    except Exception as e:
        app.logger.error(f'{asctime()} {repr(e)}')
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
