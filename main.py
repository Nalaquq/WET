from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import requests
import json

app = Flask(__name__)
bootstrap=Bootstrap5(app)
### made some edits. Might need to revert. 
KWN={
        'lon': -161.902701,
        'lat': 59.757774
        }

def set_coordinates(self): 
    longitude=self.get('lon')
    latitude=self.get('lat')
    return longitude, latitude

def get_coordinates():
    client_location = requests.get("http://ip-api.com/json/")
    response = json.loads(client_location.text)
    longitude = response["lon"]
    latitude = response["lat"]
    return longitude, latitude 

@app.route("/upload", methods=['POST'])

    
@app.route("/map", methods=['POST', 'GET'])
def root():
    try:
        client_location = requests.get("http://ip-api.com/json/")
        response = json.loads(client_location.text)
        longitude = response["lon"]
        latitude = response["lat"]

    except:
        longitude = -161.902701
        latitude = 59.757774
        pass
    if request.method=="POST":
        data=request.get_data()
        print(data)
    return render_template("index.html", longitude=longitude, latitude=latitude)

@app.route("/kwn", methods=['POST', 'GET'])
def Quinhagak():
    set_coordinates(KWN)
    return render_template("index.html", longitude=longitude, latitude=latitude)
 
    
if __name__ == "__main__":
    app.run(host="localhost", debug=True)


