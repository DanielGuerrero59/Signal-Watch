#IsolationForest being the algorithm for spotting outliers 
from sklearn.ensemble import IsolationForest
import pandas as pd


def detect_anomalies(file_path: str) -> list[dict]:
    """
    Given a CSV file with a single numeric column, flag statistical outliers.
    Returns a list of anomalies — empty list if none.
    """
    # Load the CSV into a pandas DataFrame — same "path pointing to content"
    
    df = pd.read_csv(file_path)

   #iloc is for index location, : for all rows at the first "0th" column
   # -1 to determine how many rows necessary, 1 to make it 1 column wide 
   #necessary reshape due to scikit requiring 2d input samples 
    values = df.iloc[:, 0].values.reshape(-1, 1)



    #expects 15% of data to be an anomaly, seed value to keep constant results 
    model = IsolationForest(contamination=0.15, random_state=42)

    # fit_predict does two things at once:
    # 1. FIT — analyze the data to learn what "normal" looks like
    # 2. PREDICT — label each point as +1 (normal) or -1 (anomaly)
    # This is one of scikit-learn's convenience shortcuts.
    predictions = model.fit_predict(values)

    # score_samples returns how "anomalous" each point is — more negative = weirder.
    # Flags how anomalous a point is 
    scores = model.score_samples(values)

    # Build the result: only include points labeled -1 (anomalies).
    # Loop through with enumerate() so we know the row index of each point.
    anomalies = []
    #zip to match up values, enumerate to properly count index 
    for i, (prediction, score) in enumerate(zip(predictions, scores)):
        if prediction == -1:  
            anomalies.append({
                "index": int(i),                    
                "value": float(values[i][0]),# grabs value and gets the only "1st" element in that row      
                "score": float(score),              
            })
    
    return anomalies