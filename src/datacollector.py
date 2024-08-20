import requests
import sqlite3
import json

#First let's create and connect to a SQLite3 database
connect = sqlite3.connect("playerdata.db")
cursor = connect.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS playerdata(
        playername varchar(255), 
        claywon int, 
        claylost int, 
        grasswon int, 
        grasslost int, 
        hardwon int, 
        hardlost int        
    )
""")

#Using the API URL and key below...
apikey = "4769f2b55a393a6440b6dd565f8c9375c036e73713ba0c2adf1cf0587dd8d626"
url = "https://api.api-tennis.com/tennis/?method=get_players&player_key=1910&APIkey="+apikey

#...We get the API Tennis response as a JSON (similar to Python dictionary) 
response = requests.get(url)

#We then extract a subset of the JSON to get player name and make indexing deeper values easier to write
jsonfile = json.loads(response.text)["result"][0]
playername = jsonfile["player_name"]
print("Player Name: ", playername)

stats = jsonfile["stats"]

#Initializing all surfaces win+loss counts
claywon = claylost = 0
grasswon = grasslost = 0
hardwon = hardlost = 0

#For every season (singles and doubles count separate), matches won and lost across 3 surfaces are tallied 
for entry in stats:
    entryclaywon = entry.get("clay_won") 
    if(entryclaywon != ""):
        claywon += int(entryclaywon)
    
    entryclaylost = entry.get("clay_lost") 
    if(entryclaylost != ""):
        claylost += int(entryclaylost)


    entrygrasswon = entry.get("grass_won") 
    if(entrygrasswon != ""):
        grasswon += int(entrygrasswon)

    entrygrasslost = entry.get("grass_lost") 
    if(entrygrasslost != ""):
        grasslost += int(entrygrasslost)


    entryhardwon = entry.get("hard_won") 
    if(entryhardwon != ""):
        hardwon += int(entryhardwon)
    
    entryhardlost = entry.get("hard_lost") 
    if(entryhardlost != ""):
        hardlost += int(entryhardlost)

#Now that all the information is acquired, we can add it to the playerdata table created at the start of the script
cursor.execute(
    """
    INSERT INTO playerdata (playername, claywon, claylost, grasswon, grasslost, hardwon, hardlost)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    , (playername, claywon, claylost, grasswon, grasslost, hardwon, hardlost)
)

#And finally, commit the changes and close the connection
connect.commit()
connect.close()

print("Clay matches won: ", claywon)
print("Clay matches lost: ", claylost)

print("Grass matches won: ", grasswon)
print("Grass matches lost: ", grasslost)

print("Hard matches won: ", hardwon)
print("Hard matches lost: ", hardlost)

