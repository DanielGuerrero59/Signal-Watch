import os


def save_file(filename: str, contents: bytes):
    # os.makedirs creates the uploads folder if it doesn't exist
    # exist_ok=True means don't crash if the folder is already there — just continue
    os.makedirs("uploads", exist_ok=True)

    # Builds the full path where the file will be saved e.g. "uploads/report.pdf"
    path = f"uploads/{filename}"

    # open(path, "wb") opens the file at that path in write-bytes mode
    # "wb" = write bytes — needed because files are binary data, not plain text
    # the "with" keyword automatically closes the file when we're done — no cleanup needed
    with open(path, "wb") as f:
        f.write(contents)  # Writes the raw bytes to disk

    # Returns the path so the caller knows where the file ended up
    return path