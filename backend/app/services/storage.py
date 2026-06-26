import os
import logging 
from fastapi import HTTPException
from dotenv import load_dotenv


# reading copying every line of our env file to python
load_dotenv()


logger = logging.getLogger(__name__)


def save_file(filename: str, contents: bytes):
    # os.makedirs creates the uploads folder if it doesn't exist
    # exist_ok=True means don't crash if the folder is already there — just continue
    try: 
        # using key value pair to get our value of upload folder 
        os.makedirs(os.getenv("UPLOAD_DIR"), exist_ok=True)

    



        # Builds the full path where the file will be saved e.g. "uploads/report.pdf"
        path = f"{os.getenv('UPLOAD_DIR')}/{filename}"

        # open(path, "wb") opens the file at that path in write-bytes mode
        # "wb" = write bytes — needed because files are binary data, not plain text
        # the "with" keyword automatically closes the file when we're done — no cleanup needed
        with open(path, "wb") as f:
            f.write(contents)  # Writes the raw bytes to disk

    
    except TypeError as e: 
        logger.critical(f"UPLOAD_DIR env variable not set:  {e}")
        raise HTTPException(status_code = 500, detail = "Server misconfigured: UPLOAD_DIR not set")

    except OSError as e: 
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code = 500, detail = "Failed to save file: server filesystem error")
    # Returns the path so the caller knows where the file ended up
    return path