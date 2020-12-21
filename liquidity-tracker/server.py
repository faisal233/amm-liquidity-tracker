from flask import render_template

from config import connex_app
from db import update_db, build_db

# Get the application instance
connex_app = connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    Responds to the browser URL http://localhost:5000

    :param:   n/a
    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


# Create a URL route in our application for "/tokens"
@connex_app.route("/tokens")
@connex_app.route("/tokens/<int:token_id>")

def token(token_id=""):
    """
    Responds to the browser URL http://localhost:5000/tokens

    :param:   n/a
    :return:        the rendered template "token.html"
    """
    return render_template("tokens.html", token_id=token_id)


if __name__ == "__main__":
    update_interval = 300   # updates the database after n seconds

    build_db()
    update_db(update_interval)
    connex_app.run()
