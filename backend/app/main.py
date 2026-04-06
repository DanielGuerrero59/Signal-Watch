from fastapi import FastAPI  
# fastapi is the module(toolbox), 
# from keyword in python is typically used to import specific items from a module 
# we are importing the FastAPI class from the fastapi module/TOOLBOX

app = FastAPI(title="SignalWatch")  # creates actual server object, app is our instance 
# the constructor has optional arguments, and we use the keyword way of assigning the value directly 
# possible in python ^^^


@app.get("/health")  # decorator function 
def health_check():   #standard python function syntax 
    return {"status": "ok"}      


@app.get("/about", status_code= 200)  #code 200 to allow client to know data has been sent back 
def about_check(): 
    return {
        "project" : "SignalWatch",
        "version" :  "1",
        "description" : "Ingests media to human insight"
        }



@app.get("/status", status_code =200) 
def status(): 
    return {
        "Start Time" : "4/6/2026"
    }

