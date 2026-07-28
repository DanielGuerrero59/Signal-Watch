import logging
from app.database import SessionLocal
from app.models import Upload
from app.services.summarize import summarize_text

logger = logging.getLogger(__name__)


def process_upload(upload_id: int):
    """Background task: read the uploaded file, summarize it, save the summary."""
    
    # Open a fresh DB session — the request's session is gone by now
    db = SessionLocal()
    
    try:
        # 1. Fetch the row we're processing
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if upload is None:
            logger.error(f"Upload {upload_id} not found")
            return
        
        # 2. Read the file (only handle .txt for now)
        if upload.file_type != ".txt":
            logger.info(f"Skipping summarization for {upload.file_type} — not supported yet")
            return
        
        with open(upload.path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # 3. Summarize
        summary = summarize_text(text)  # ← your line: call summarize_text with the text you just read
        
        # 4. Save it to the row
        upload.summary = summary  # ← your line: assign the summary to the row's column
        db.commit()           
        
        logger.info(f"Summarized upload {upload_id}")
    
    except Exception as e:
        # Broad catch on purpose — background tasks shouldn't crash silently or loudly
        logger.error(f"Failed to summarize upload {upload_id}: {e}")
    
    finally:
        db.close()   # ← always close the session, even on error