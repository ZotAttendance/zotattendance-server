from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    '''Send index.html when users entered the root URL.'''
    return send_from_directory("static", "index.html")

@app.route("/assets/<static_file>")
def assets(static_file):
    '''Send other static files like images under the assets/ directory.'''
    return send_from_directory("static/assets", static_file)

@app.route("/api/login", methods=['POST'])
def api():
    return jsonify({
        "success": False,
        "message": "testing"
    })

if __name__ == "__main__":
    app.run()