import requests
import json
import os
from flask import Flask, jsonify, render_template, request, send_from_directory
app = Flask(__name__)

grad = {
    "standart": "°K",
    "imperial": "°F",
    "metric"  : "°C"
}

APIKEY = ""
with open("apikey.txt", "r") as f:
  APIKEY = f.read()

forecastexclude = "minutly,daily"
language = "de"

def api_call_stadt():
    stadt         = request.args["stadt"] if request.args.__contains__("stadt") else ""
    units         = request.args['units'] if request.args.__contains__('units') else "metric"

    cords         = requests.post(f"https://api.openweathermap.org/data/2.5/weather?q={stadt}&lang={language}&appid={APIKEY}").json()
    data          = requests.post(f"https://api.openweathermap.org/data/2.5/onecall?lat={cords['coord']['lat']}&lon={cords['coord']['lon']}&exclude={forecastexclude}&units={units}&lang={language}&appid={APIKEY}").json() if cords["cod"] == 200 else cords
    data["grad"]  = grad.get(units)
    data["name"]    = cords["name"] if cords["cod"] == 200 else ""
    data["cod"]     = cords["cod"]
    data["curtemp"] = round(float(data["current"]["temp"])) if cords["cod"] == 200 else ""
    return data 

def api_call_position():
    lat             = request.args["lat"] if request.args.__contains__("lat") else ""
    lon             = request.args["long"] if request.args.__contains__("long") else ""
    units           = request.args['units'] if request.args.__contains__('units') else "metric"

    cords           = requests.post(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang={language}&appid={APIKEY}").json()
    data            = requests.post(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={forecastexclude}&units={units}&lang={language}&appid={APIKEY}").json()
    data["grad"]    = grad.get(units)
    data["name"]    = cords["name"] if cords["cod"] == 200 else ""
    data["cod"]     = cords["cod"]
    data["curtemp"] = round(float(data["current"]["temp"])) if cords["cod"] == 200 else ""
    return data

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.args.__contains__("stadt"):
        data = api_call_stadt()
    elif request.args.__contains__("position"):
        data = api_call_position()
    else:
        data = 400
    return render_template("index.html", data=data)

@app.route('/favicons/favicon256.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/facivons'),
                               'favicon256-von-icons8.png', mimetype='image/png')
if __name__ == "__main__":
    app.run(debug=True, port=443, host="0.0.0.0", ssl_context=("certificate/cert.pem", "certificate/key.pem"))
