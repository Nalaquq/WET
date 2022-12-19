from flask import Flask, render_template, request

app = Flask(__name__)


def make_user_map():
    def locate_user():
        try:
            client_location = requests.get("http://ip-api.com/json/")
            response = json.loads(client_location.text)
            u_long = response["lon"]
            u_lat = response["lat"]
        except:
            pass

    locate_user()


make_user_map()


@app.route("/")
def root():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
