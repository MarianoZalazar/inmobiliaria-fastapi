from flask import Flask, json
import mongodb as db


def get_json(dictionary):
    return app.response_class(response=json.dumps(dictionary), status=200, mimetype="application/json")


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello Flask"


@app.route('/api/<string:barrio>')
def barrio(barrio):
    propiedades = db.buscar_por_barrio(barrio.lower())
    return get_json(propiedades)


@app.route('/api/<string:barrio>/<string:inmueble>')
def barrio_inmueble(barrio, inmueble):
    propiedades = db.buscar_por_barrio_inmueble(
        barrio.lower(), inmueble.lower())
    return get_json(propiedades)


@app.route('/api/<string:barrio>/<string:inmueble>/<string:tipo>')
def barrio_inmueble_tipo(barrio, inmueble, tipo):
   propiedades = db.buscar_por_barrio_inmueble_tipo(
       barrio.lower(), inmueble.lower(), tipo.lower())
   return get_json(propiedades)


if __name__ == '__main__':
    app.run(port=db.PORT)
