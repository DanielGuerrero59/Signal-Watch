from fastapi import FastAPI  
# fastapi is the module(toolbox), 
# from keyword in python is typically used to import specific items from a module 
# we are importing the FastAPI class from the fastapi module/TOOLBOX

app = FastAPI(title="SignalWatch")  # creates actual server object, app is our instance 
# the constructor has optional arguments, and we use the keyword way of assigning the value directly 
# possible in python ^^^


@app.get("/health")  # decorator function 
#.get() is a built in function from fastapi to handle get requests from HTTP


def health_check():   #standard python function syntax 
    return {"status": "ok"}         
