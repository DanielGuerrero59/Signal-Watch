import os
import logging
from fastapi import HTTPException
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)


async def save_file(file, filename: str, max_size: int, chunk_size: int = 1024 * 1024):
    try:
        # Ensure uploads directory exists
        os.makedirs(os.getenv("UPLOAD_DIR"), exist_ok=True)

        # Full path where the file will land
        path = f"{os.getenv('UPLOAD_DIR')}/{filename}"

        total_size = 0
        too_large = False

        # Open the destination file, stream chunks into it
        with open(path, "wb") as f:
            while True:
                chunk = await file.read(chunk_size)
                # Stream exhausted — no more data
                if not chunk:
                    break

                total_size += len(chunk)

                # Enforce max size mid-stream — abort and clean up if exceeded
                if total_size > max_size:
                    too_large = True
                    break

                f.write(chunk)


        if too_large: 
            os.remove(path)
            raise HTTPException(status_code = 413, detail = "File Too Large")

        # Empty file guard — checked AFTER writing (file is 0 bytes on disk)
        if total_size == 0:
            os.remove(path)
            raise HTTPException(status_code=400, detail="File is Empty")

    except TypeError as e:
        logger.critical(f"UPLOAD_DIR env variable not set: {e}")
        raise HTTPException(status_code=500, detail="Server misconfigured: UPLOAD_DIR not set")

    except OSError as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save file: server filesystem error")

    return path, total_size