from sklearn.ensemble import IsolationForest
import pandas as pd


def detect_anomalies(file_path: str) -> list[dict]:
    """
    Given a CSV file with a single numeric column, flag statistical outliers.
    Returns a list of anomalies — empty list if none.
    """
    # Load the CSV into a pandas DataFrame — same "path pointing to content"
    
    df = pd.read_csv(file_path)

   
    values = df.iloc[:, 0].values.reshape(-1, 1)



    
    model = IsolationForest(contamination=0.15, random_state=42)

    # fit_predict does two things at once:
    # 1. FIT — analyze the data to learn what "normal" looks like
    # 2. PREDICT — label each point as +1 (normal) or -1 (anomaly)
    # This is one of scikit-learn's convenience shortcuts.
    predictions = model.fit_predict(values)

    # score_samples returns how "anomalous" each point is — more negative = weirder.
    # We use this so the API response tells the user HOW anomalous each flagged point is.
    scores = model.score_samples(values)

    # Build the result: only include points labeled -1 (anomalies).
    # Loop through with enumerate() so we know the row index of each point.
    anomalies = []
    for i, (prediction, score) in enumerate(zip(predictions, scores)):
        if prediction == -1:  # -1 means anomaly, +1 means normal
            anomalies.append({
                "index": int(i),                    # which row in the CSV
                "value": float(values[i][0]),       # the actual value
                "score": float(score),              # how weird (more negative = weirder)
            })
    # Cast to Python-native types (int/float) so JSON serialization works —
    # numpy's int64 and float64 aren't JSON-serializable by default.

    return anomalies