from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, distinct
import pandas as pd
import requests
from dotenv import load_dotenv, dotenv_values 
import os
import json

#Importing the db and objects created for this project in models.py
from models import db, Match, Player

main = Blueprint("main", __name__)
def create_app():
    print("entering create_app()")
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)
    app.register_blueprint(main)
    return app

@main.route("/")
def index():
    print("entering index()")
    load_match_data()
    return render_template("index.html")

@main.route("/search")
def search():
    print("entering search()")
    q = request.args.get("q")
    #If some input is entered:
    if q:
        results = Match.query.filter(Match.winner_name.icontains(q) | Match.loser_name.icontains(q))\
        .limit(100).all()

        validplayer = db.session.query(func.count(distinct(Match.winner_name))).filter\
        (func.lower(Match.winner_name)==func.lower(q)).scalar()
        playerresult = Player()
        #If some input is entered that matches exactly 1 player:
        if(validplayer==1):
            #Loading the live ATP ranking data from the Sportradar API and clean json to return only player names and ranks (function defined below)
            r = load_ranking_data()[q.lower()]
            clayW = db.session.query(func.count(Match.id)).filter\
                (func.lower(Match.winner_name)==func.lower(q), Match.surface=="Clay").scalar()
            clayL = db.session.query(func.count(Match.id)).filter\
                (func.lower(Match.loser_name)==func.lower(q), Match.surface=="Clay").scalar()
            
            grassW = db.session.query(func.count(Match.id)).filter\
                (func.lower(Match.winner_name)==func.lower(q), Match.surface=="Grass").scalar()
            grassL = db.session.query(func.count(Match.id)).filter\
                (func.lower(Match.loser_name)==func.lower(q), Match.surface=="Grass").scalar()
            
            hardcourtW = db.session.query(func.count(Match.id)).filter\
                (func.lower(Match.winner_name)==func.lower(q), Match.surface=="Hard").scalar()
            hardcourtL = db.session.query(func.count(Match.id)).filter\
                (func.lower(Match.loser_name)==func.lower(q), Match.surface=="Hard").scalar()
            
    else:
        results = []
    playerresult = Player(name=q.title(), rank=r, cw=clayW, cl=clayL, gw=grassW, gl=grassL, hcw=hardcourtW, hcl=hardcourtL)
    return render_template("search_results.html", results=results, playerresult=playerresult)

# Import and run this function in flask shell after creating the database
def load_match_data():
    print("entering load_match_data()")
    #Loading the internal csv containing 5 years of ATP match data
    rawdf = pd.read_csv("rawdata/atp_2019_2023.csv")
    cleandf = rawdf.filter(['tourney_name', 'tourney_date', 'surface', 'match_num', 'winner_name', 'loser_name', 'score'], axis=1)
    cleandf = cleandf.fillna(value="None")
    for i in cleandf.index:
        tn = cleandf["tourney_name"][i]
        #Getting date in a more readable format
        rawdate = str(cleandf["tourney_date"][i])
        td = rawdate[:4] + "-" + rawdate[4:6] + "-" + rawdate[6:]
        su = cleandf["surface"][i]
        mn = int(cleandf["match_num"][i])
        wn = cleandf["winner_name"][i]
        ln = cleandf["loser_name"][i]
        sc = cleandf["score"][i]
        #Creating a match object with all the relevant info of the dataframe row, so it can easily be added as one object in the database
        match = Match(tourney_name=tn, tourney_date=td, surface=su, match_num=mn, winner_name=wn, loser_name=ln, score=sc)
        db.session.add(match)
    db.session.commit()

def load_ranking_data():
    print("entering load_ranking_data()")
    if(os.path.exists("rawdata/rankings.json")):
        print("JSON already exists")
    else:
        print("Calling API, saving new JSON")
        load_dotenv()
        apikey = os.getenv("SportRadarAPI")
        url = "https://api.sportradar.com/tennis/trial/v3/en/rankings.json?api_key="+apikey
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        responsedict = response.json()
        with open("rawdata/rankings.json", "w") as rankings:
            json.dump(responsedict, rankings)
    
    #Cleaning raw JSON to extract just player names and ranks
    with open("rawdata/rankings.json", "r") as rankings:
        responsedict = json.load(rankings)
        #ATP (mens) ranking dictionary, top 500
        rawrankingdict = responsedict["rankings"][0]["competitor_rankings"]
        cleanrankingdict = {}
        for i in range(len(rawrankingdict)):
            cleanname = rawrankingdict[i]["competitor"]["name"].split(", ")
            cleanfirstname = cleanname[1]
            cleanlastname = cleanname[0]
            cleanname = (cleanfirstname + " " + cleanlastname).lower() 
            cleanrankingdict[cleanname] = rawrankingdict[i]["rank"]

        return cleanrankingdict