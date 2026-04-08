#TestClient is a fake browser sending requests- without needing the server to be running 
# goes to app folder to main.py and imports our app server variable 
from fastapi.testclient import TestClient  
from app.main import app 


#creates fake browser pointed at our app
client = TestClient(app) 

def test_health_check(): 
    response = client.get("/health")
    assert response.status_code == 200 
    assert response.json() == {"status": "ok"} 


def test_about_check(): 
    info = client.get("/about")
    assert info.status_code == 200 
    assert info.json() == {
        "project" : "SignalWatch",
        "version" :  "1",
        "description" : "Ingests media to human insight"
        }


def test_status(): 
    check = client.get("/status")
    assert check.status_code == 200 

def test_upload_valid(): 
    
