import os
import pytest
from app import create_app, index, search, load_match_data, load_ranking_data
from dotenv import load_dotenv, dotenv_values 
import requests

#Creating Flask app instance for testing purposes
@pytest.fixture
def testapp():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def testclient(testapp):
    return testapp.test_client()

@pytest.fixture
def rankurl():
    load_dotenv()
    apikey = os.getenv("SportRadarAPI")
    return "https://api.sportradar.com/tennis/trial/v3/en/rankings.json?api_key="+apikey

def test_create_app():
    assert create_app() != None

def test_index(testclient):
    with create_app().app_context():
        assert index() != None
    response = testclient.get('/')
    assert response.status_code == 200

def test_load_ranking_data(rankurl):
    response = requests.get(rankurl)
    assert response.status_code == 200

def test_load_match_data():
    assert os.path.exists("rawdata/atp_2019_2023.csv")
    assert os.path.exists("instance/db.sqlite3")

def test_search(testclient):
    assert os.path.exists("rawdata/rankings.json")   
    response = testclient.get('/search?q=Jannik%20Sinner')   
    assert response.status_code == 200
    assert b'Jannik Sinner' in response.data
    