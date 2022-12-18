from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
import requests
import os
import folium as fl
import json
import leafmap

app = Flask(__name__)

bootstrap = Bootstrap(app)


def make_user_map():
    def locate_user():
        try:
            client_location = requests.get("http://ip-api.com/json/")
            response = json.loads(client_location.text)
            u_long = response["lon"]
            u_lat = response["lat"]
            folium_map = fl.Map(
                location=[u_lat, u_long],
                zoom_start=13,
                tiles="cartodbpositron",
                width="75%",
                height="75%",
            )
            folium_map.save("templates/index.html")
        except:  # loads Quinhagak coordinates if lacking internet
            folium_map = fl.Map(
                location=[59.7488889, -161.9020],
                zoom_start=13,
                tiles="cartodbpositron",
                width="75%",
                height="75%",
            )
            folium_map.save("templates/index.html")
            pass

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
