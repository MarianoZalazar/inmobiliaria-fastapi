from flask import Flask, json
from mongodb import PORT

def get_json(dictionary):
    return app.response_class(response = json.dumps(dictionary), status = 200, mimetype = "application/json")

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Flask"

if __name__ == '__main__':
    app.run(port = PORT, debug = True, host="0.0.0.0")