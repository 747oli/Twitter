import tweepy
from twitterApp import app
from flask import render_template, redirect, url_for, request, get_flashed_messages
from twitterApp.Forms import LoginForm, AuthoriseForm
import os
import webbrowser
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
            webbrowser.open_new_tab(redirect_url)
            return redirect(url_for('authorise')(auth))
        except tweepy.TweepyException:
            print('Error! Failed to get request token.')
            return render_template("login.html", form=form,active=True)
    return render_template("login.html", form=form,active=True)

@app.route("/logout")
def logout():
    return render_template("logout.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", )

@app.route("/authorise", methods=["GET", "POST"])
def authorise():
    form = AuthoriseForm()
    if request.method == "POST":
        token = request.form["autorisation_key"]
        try:
            access = auth.get_access_token(token)
            print(access)
        except:
            pass
    return render_template("authorise.html", form=form, auth = request.args.get('email'))