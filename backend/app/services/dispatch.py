from app.database import SessionLocal
from app.models import Upload
from app.services.summarize import summarize_text
from app.services.transcribe import transcribe_audio
import traceback


def run_ai_pipeline(upload_id: int, file_path: str, extension: str) -> None:
    """Route an uploaded file to the correct AI pipeline and save results to DB."""
    print(f"[DISPATCH] Starting pipeline for upload_id={upload_id}, ext={extension}, path={file_path}")
    db = SessionLocal()
    try:
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        print(f"[DISPATCH] Found upload row: {upload}")

        if extension in {".pdf", ".txt"}:
            print("[DISPATCH] Routing to summarizer...")
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            upload.summary = summarize_text(text)
            print("[DISPATCH] Summary generated")

        elif extension in {".mp3", ".wav", ".m4a"}:
            print("[DISPATCH] Routing to transcriber...")
            upload.transcript = transcribe_audio(file_path)
            print(f"[DISPATCH] Transcript generated: {upload.transcript[:60]}...")

        db.commit()
        print("[DISPATCH] Committed to DB")
    except Exception as e:
        # Background tasks swallow exceptions silently — this forces them to print
        print(f"[DISPATCH ERROR] {type(e).__name__}: {e}")
        traceback.print_exc()
    finally:
        db.close()
        print("[DISPATCH] DB session closed")