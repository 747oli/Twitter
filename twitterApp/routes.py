import tweepy
from twitterApp import app
from flask import render_template, redirect, url_for, request, get_flashed_messages
from twitterApp.Forms import LoginForm, AuthoriseForm
import os
import webbrowser
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

class Auth():
    def __init__(self, consumer_key = None, consumer_secret = None):
        self.auth = None
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback_uri = "oob"

    def setConsumer_key(self, consumer_key):
        self.consumer_key = consumer_key
        return self.consumer_key

    def setconsumer_secret(self, consumer_secret):
        self.consumer_secret = consumer_secret
        return self.consumer_secret

    def setAuth(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.callback_uri)
        return self.auth

    def getAuth(self):
        return self.auth

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        A1.setConsumer_key(request.form["consumer_key"])
        A1.setconsumer_secret(request.form["consumer_secret"])
        access_token = request.form["access_token"]
        access_token_secret = request.form["access_token_secret"]
        try:
            A1.setAuth()
            A1.setAuth()
            auth = A1.getAuth()
            redirect_url = auth.get_authorization_url()
            webbrowser.open_new_tab(redirect_url)
            return redirect(url_for("authorise"))
        except tweepy.TweepyException:
             print('Error! Failed to get request token.')
        return render_template("login.html", form=form, active=True)
    return render_template("login.html", form=form ,active=True)

@app.route("/logout")
def logout():
    return render_template("logout.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/authorise", methods=["GET", "POST"])
def authorise():
    form = AuthoriseForm()
    if request.method == "POST":
        token = request.form["autorisation_key"]
        try:
            auth = A1.getAuth()
            access = auth.get_access_token(token)
            return redirect(url_for("dashboard"))
        except:
            print('Error! Failed to get request authorisation.')
    return render_template("authorise.html", form=form, auth = request.args.get('email'))

A1 = Auth()