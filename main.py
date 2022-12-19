from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


#Need to rewrite so it passes longitude and latitude outside function
def location_API():
    try:
        client_location = requests.get("http://ip-api.com/json/")
        response = json.loads(client_location.text)
        longitude = response["lon"]
        latitude = response["lat"]
    except:
        longitude=-161.902701
        latitude=59.757774
        pass

@app.route("/")
def root():
    try:
        client_location = requests.get("http://ip-api.com/json/")
        response = json.loads(client_location.text)
        longitude = response["lon"]
        latitude = response["lat"]
    except:
        longitude=-161.902701
        latitude=59.757774
        pass
    return render_template("index.html", longitude=longitude, latitude=latitude)

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
