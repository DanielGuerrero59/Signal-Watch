import os 


def save_file(filename: str, contents: bytes):
    #os.makedirs creates folder and exist_ok makes sure if it already exists to just resume 
    os.makedirs("uploads", exist_ok = True) 

    path = f"uploads/{filename}"
    #write bytes = wb 
    #with keyword closes path immediately for us when exiting 
    with open(path, "wb") as f: 
        f.write(contents)
    return path
    
