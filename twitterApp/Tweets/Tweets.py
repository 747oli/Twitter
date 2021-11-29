from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Tweets():
    def __init__(self):
        self.members = []
        self.statusses = []
        self.crypto = ["BTC", "Cardano", "Tether" ,"Doge", "bitcoin", "Etherium", "Altcoin", "Blockchain", "Coin", "Cryptocurrency", "Token", "Crypto", "Binance"]
        self.market = ["market", "stock", "NYSE", "NASDAQ", "points", "ticker", "NSDQ", "Dow Jones", "index", "futures"]
        self.myStocks = ["Visa", "V", "MCDO", "McDonalds", "PEPSI", "MSFT", "Microsoft"]
        self.analyzer = SentimentIntensityAnalyzer()
        self.sentimentList = []

    def set_Sentiment(self, tweet):
        polarity_scores = self.analyzer.polarity_scores(tweet)
        sentiment = polarity_scores["compound"]
        self.addToSentimentList(sentiment)
        return sentiment

    def addToSentimentList(self, sentiment):
        self.sentimentList.append(sentiment)
        return self.sentimentList

    def get_total_sentiment(self):
        totaalSentiment = 0
        aantal = 0
        for sentiment in self.sentimentList:
            totaalSentiment += (sentiment * 100)
            aantal +=1
        gemiddeldSentiment = totaalSentiment/aantal
        return gemiddeldSentiment

    def resetLists(self):
        self.sentimentList = []
        self.statusses = []


T1 = Tweets()