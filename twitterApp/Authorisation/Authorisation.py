import tweepy

class Auth():
    def __init__(self):
        self.auth = None
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.callback_uri = "oob"
        self.api = None
        self.error = None


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

A1 = Auth()