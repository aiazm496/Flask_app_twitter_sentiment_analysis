from flask import Flask,render_template,request
import tweepy
from tweepy.api import API
import credentials
from textblob import TextBlob
import matplotlib.pyplot as plt

app = Flask(__name__)

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY,credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth=auth)


@app.route('/home',methods = ['GET','POST'])
def home():
    if request.method == 'POST':
       tweet_keyword = request.form['keyword']
       #print(tweet_keyword)
       tweet_data = api.search_tweets(tweet_keyword,count = 50)
       neg = 0
       pos = 0
       neu = 0
       for tweet in tweet_data:
           blob = TextBlob(tweet.text)
           if blob.sentiment.polarity < 0:
               neg+=1
           elif blob.sentiment.polarity == 0:
               neu +=1
           else:
               pos+=1

       plt.pie([neg,pos,neu],labels=['negative','positive','neutral'],autopct='%.1f%%')
       plt.savefig('static/pie_chart_{}.png'.format(tweet_keyword))
       plt.close()
       

       return render_template('home_result.html',image_src ='pie_chart_{}.png'.format(tweet_keyword))
    else:    
        return render_template('home.html')





if __name__ == "__main__":
    app.run(debug=True)

