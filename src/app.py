from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

@app.route("/")
def home():
    return "🌤️ Welcome to the Weather API! Use /weather?lat=<lat>&lon=<lon> to get current weather."

@app.route("/weather")
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Missing lat or lon"})
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto"
    }

    response = requests.get(BASE_URL, params=params)

    return jsonify(response.json())

    #start the server with:
    #start python src/app.py
    # curl http://localhost:5000/weather?lat=-30.709675&lon=134.568701