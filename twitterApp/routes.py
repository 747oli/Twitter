import tweepy
from twitterApp import app
from flask import render_template, redirect, url_for, request, get_flashed_messages
from twitterApp.Forms import LoginForm
import os
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        consumer_key = request.form["consumer_key"]
        consumer_secret = request.form["consumer_secret"]
        access_token = request.form["access_token"]
        access_token_secret = request.form["access_token_secret"]
        try:
            callback_uri = "oob"
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
            redirect_url = auth.get_authorization_url()
            print(redirect_url)
            return redirect(url_for('dashboard', redirect_url =redirect_url))
        except tweepy.TweepyException:
            print('Error! Failed to get request token.')
            return render_template("login.html", form=form,active=True)
    return render_template("login.html", form=form,active=True)

@app.route("/logout")
def logout():
    return render_template("logout.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", redirect_url = request.args.get("redirect_url"))
