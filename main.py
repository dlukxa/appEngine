from flask  import Flask, render_template
from pymongo import MongoClient
import requests
from flask import request,jsonify
from newsapi import NewsApiClient
from GoogleNews import GoogleNews
import json

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.weekTopic

def userRegistor():
    try:
        #IP = request.remote_addr
        db.users.create_index([("user_ip")], unique=True)
        user = db.users.insert_one({'user_ip': '112.134.183.15'})
        return user['_id']
    except Exception as e:
        user = db.users.find_one({'user_ip': '112.134.183.15'})
        #print(user['_id'])
        return user['_id']
    
def userDetails():
    try:
        #IP = requests.remote_addr
        response = requests.get("http://ip-api.com/json/{}".format('113.134.183.15'))
        js = response.json()
        usrLogin = db.usersLogin.insert_one(js)
        return usrLogin['_id']
    except Exception as e:
        return False

def newsApi(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey=a270a304d8f940e791565dfadcc16d48"
    response = requests.get(url)
    data = response.json()
    db.newsApi.insert_many(data['articles'])
    return data

def googlenewsApi(query):
    # Init
    googlenews = GoogleNews(lang='en', period='1d')
    googlenews.search("Bitcoin")
    results = googlenews.results(sort=True)
    return results

@app.route("/")
def home():
    userID = userRegistor()
    return jsonify({'ip': request.remote_addr}), 200

@app.route("/api/newsapi/")
def Newsapi():
    sources = newsApi("Bitcoin")
    return jsonify(sources), 200

@app.route("/api/googlenewsapi/")
def googlenewsApi():
    sources = googlenewsApi("Bitcoin")
    return jsonify(sources), 200

if __name__ == "__main__":
    app.run(debug=True)