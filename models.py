from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Each row of the Match database encompasses one Match object
class Match(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    tourney_name     = db.Column(db.String(100), nullable=False)
    tourney_date     = db.Column(db.String(100), nullable=False)
    surface          = db.Column(db.String(100), nullable=False)
    match_num        = db.Column(db.Integer)
    winner_name      = db.Column(db.String(100), nullable=False)
    loser_name       = db.Column(db.String(100), nullable=False)
    score            = db.Column(db.String(100), nullable=False) 

#Attributes of the player are populated after querying
class Player():
    def __init__(self, name=0, rank=0, cw=0, cl=0, gw=0, gl=0, hcw=0, hcl=0):
        self.name = name
        self.rank = rank
        #Start with all surface winrates = 0 (to be calculated after object initialized)
        self.cwrate = self.gwrate = self.hcwrate = self.wrate = 0
        #Clay wins, losses, sum, and winrate
        self.cw = cw
        self.cl = cl
        self.c = cw+cl
        if(self.c>0):
            self.cwrate = round(self.cw/self.c, 5)
        #Grass wins, losses, sum, and winrate
        self.gw = gw
        self.gl = gl
        self.g = gw+gl
        if(self.g>0):
            self.gwrate = round(self.gw/self.g, 5)
        #Hardcourt wins, losses, sum, and winrate
        self.hcw = hcw
        self.hcl = hcl        
        self.hc = hcw+hcl
        if(self.hc>0):
            self.hcwrate = round(self.hcw/self.hc, 5)

        #Total wins and total matches
        self.tw = cw+gw+hcw
        self.tm = self.c+self.g+self.hc
        if(self.tm>0):
            self.wrate = round((self.tw)/(self.tm), 5)