from flask import Flask, json
import mongodb as db

def get_json(dictionary):
    return app.response_class(response = json.dumps(dictionary), status = 200, mimetype = "application/json")

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello Flask"

@app.route('/api/<string:barrio>')
def barrio(barrio):
    propiedades_por_barrio = db.buscar_por_barrio(barrio.lower())
    return get_json(propiedades_por_barrio)

@app.route('/api/<string:barrio>/<string:tipo>')
def tipo(barrio, tipo):
    propiedades_por_barrio_y_tipo = db.buscar_por_barrio_y_tipo(barrio.lower(), tipo.lower())
    return get_json(propiedades_por_barrio_y_tipo)

if __name__ == '__main__':
    app.run(port = PORT, debug = True, host="0.0.0.0")