import tweepy
from twitterApp import app
from flask import render_template, redirect, url_for, request, get_flashed_messages
from twitterApp.Forms import LoginForm, AuthoriseForm, SearchForm
import os
import re
import webbrowser
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

class Auth():
    def __init__(self):
        self.auth = None
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.callback_uri = "oob"
        self.api = None


    def setConsumer_key(self, consumer_key):
        self.consumer_key = consumer_key
        return self.consumer_key

    def setConsumer_secret(self, consumer_secret):
        self.consumer_secret = consumer_secret
        return self.consumer_secret

    def setAuth(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.callback_uri)
        return self.auth

    def getAuth(self):
        return self.auth

    def setAccess_token(self, access_token):
        self.access_token = access_token
        return self.access_token

    def setaccess_token_secret(self, access_token_secret):
        self.access_token_secret = access_token_secret
        return self.access_token_secret

    def setApi(self):
        self.api = tweepy.API(self.auth)
        return self.api

    def getApi(self):
        return self.api

@app.route('/')
def home():
    if A1.getApi():
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        A1.setConsumer_key(request.form["consumer_key"])
        A1.setConsumer_secret(request.form["consumer_secret"])
        try:
            A1.setAuth()
            auth = A1.getAuth()
            redirect_url = auth.get_authorization_url()
            webbrowser.open_new_tab(redirect_url)
            return redirect(url_for("authorise"))
        except tweepy.TweepyException:
             print('Error! Failed to get request token.')
        return render_template("login.html", form=form, active=True)
    return render_template("login.html", form=form ,active=True)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    form = SearchForm()
    statusses = []
    if request.method == "POST":
        word = f"({request.form['searchField']})"
        list_id = 1463104625704378368
        members = A1.api.list_timeline(list_id=list_id, include_rts=False)

        for member in members:
            status = A1.api.get_status(member.id, tweet_mode="extended")
            print(status.full_text)
            match = re.search(word, status.full_text)
            if match:
                statusses.append(status)
                print("Found")
            else:
                pass

        return render_template("dashboard.html", statusses=statusses, form=form)

    return render_template("dashboard.html", statusses = statusses, form=form)

@app.route("/authorise", methods=["GET", "POST"])
def authorise():
    form = AuthoriseForm()
    if request.method == "POST":
        token = request.form["autorisation_key"]
        try:
            auth = A1.getAuth()
            access = auth.get_access_token(token)
            A1.setAccess_token(access[0])
            A1.setaccess_token_secret(access[1])
            api = A1.setApi()
            return redirect(url_for("dashboard"))
        except:
            print('Error! Failed to get request authorisation.')
    return render_template("authorise.html", form=form)

@app.route("/logout")
def logout():
    A1.api = None
    return redirect(url_for("home"))

A1 = Auth()