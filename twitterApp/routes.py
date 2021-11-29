import tweepy
from twitterApp import app
from flask import render_template, redirect, url_for, request

from twitterApp.Forms.Forms import LoginForm, AuthoriseForm, SearchForm
from twitterApp.Authorisation.Authorisation import A1
from twitterApp.Tweets.Tweets import T1

import os
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

import re
import webbrowser
import plotly.graph_objects as go

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
            A1.error = None
            return redirect(url_for("authorise"))
        except tweepy.TweepyException as e:
            A1.error = e
            print(e)
        return redirect(url_for("login"))
    return render_template("login.html", form=form ,active=True, error = A1.error, loginActive=True)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    form = SearchForm()

    if request.method == "POST":
        list_id = 1463104625704378368
        T1.members = A1.api.list_timeline(list_id=list_id, include_rts=False, count=200)

        if request.form["btn"] == "search":
            T1.statusses = []
            T1.sentimentList = []

            word = f"({request.form['searchField']})"
            for member in T1.members:
                status = A1.api.get_status(member.id, tweet_mode="extended")
                match = re.search(word, status.full_text, flags=re.IGNORECASE)
                if match:
                    T1.statusses.append(status)
                    T1.set_Sentiment(status.full_text)
                else:
                    pass
        elif request.form["btn"] == "loop":
            selected = request.form.get("select")

            T1.statusses = []
            T1.sentimentList = []
            list = []

            if selected == "1":
                list = T1.crypto
            elif selected == "2":
                list = T1.market
            elif selected == "3":
                list = T1.myStocks

            for member in T1.members:
                appended = False
                status = A1.api.get_status(member.id, tweet_mode="extended")
                for word in list:
                    match = re.search(word, status.full_text, re.IGNORECASE)
                    if match and not appended:
                        T1.statusses.append(status)
                        T1.set_Sentiment(status.full_text)
                        appended = True
                    else:
                        pass
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", statusses = T1.statusses, form=form, dashboardActive=True ,sentimentActive= False)

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
            A1.setApi()
            A1.error = None
            return redirect(url_for("dashboard"))
        except tweepy.TweepyException as e:
            A1.error = e
        return redirect(url_for("authorise"))
    return render_template("authorise.html", form=form, error = A1.error)

@app.route("/logout")
def logout():
    A1.api = None
    return redirect(url_for("home"))

@app.route("/sentiment")
def sentiment():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=T1.get_total_sentiment(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sentiment"},
        gauge = {'axis': {'range': [-100, 100]},
                 'bar': {'color': "grey"},
             'steps': [
                 {'range': [-100, -50], 'color': "red"},
                 {'range': [-50, 50], 'color': "white"},
                 {'range': [50, 100], 'color': "green"}]}))

    fig.write_image("twitterApp/static/src/fig.png")

    return render_template("sentiment.html", fig = fig, dashboardActive=False ,sentimentActive= True)


