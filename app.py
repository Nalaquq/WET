from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
import requests
import os
import folium as fl
import json

app = Flask(__name__)

bootstrap = Bootstrap(app)

def make_user_map(): 
    def locate_user():
        client_location=requests.get('http://ip-api.com/json/')
        response=json.loads(client_location.text)
        u_long=(response['lon'])
        u_lat=(response['lat'])
        ###add try/except block in case internet does not work
        folium_map=fl.Map(location=[u_lat, u_long], zoom_start=13, tiles='cartodbpositron', width='75%', height='75%')
        folium_map.save('templates/index.html')
    locate_user()

make_user_map()

@app.route("/")
def login():
    return render_template("base.html")

@app.route("/home")
def index():
    return render_template("base.html")

@app.route("/start")
def start():
    return render_template("base.html")


@app.route("/map")
def select():
    return render_template("map_template.html")


if __name__ == "__main__":
    app.run(debug=True)
