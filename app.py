from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
import requests

app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/start")
def index():
    return render_template("base.html")


@app.route("/select")
def index():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
