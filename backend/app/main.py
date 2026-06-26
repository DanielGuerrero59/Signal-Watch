from fastapi import FastAPI
# Imports the router we defined in upload.py so main.py knows about those routes

import logging 

from app.routes.upload import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FastAPI is the module (toolbox)
# We are importing the FastAPI class from the fastapi module
app = FastAPI(title="SignalWatch")  # Creates the actual server object — app is our instance

# Attaches the upload router to our app
# Without this line, none of the routes in upload.py would be reachable
app.include_router(router)

# Decorator registers health_check as the handler for GET /health
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Returns basic project info — useful for anyone consuming the API to know what they're talking to
@app.get("/about", status_code=200)
def about_check():
    return {
        "project": "SignalWatch",
        "version": "1",
        "description": "Ingests media to human insight"
    }

# Returns operational info like when the project started
@app.get("/status", status_code=200)
def status():
    return {
        "Start Time": "4/6/2026"
    }