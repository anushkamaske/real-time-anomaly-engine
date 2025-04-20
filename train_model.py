import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'anomaly_model.joblib')

def load_data(path='data/historical.csv'):
    return pd.read_csv(path)

def train_and_save():
    df = load_data()
    features = df[['feature1', 'feature2', 'feature3']]
    model = IsolationForest(
        n_estimators=100,
        contamination=0.01,
        random_state=42
    )
    model.fit(features)
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == '__main__':
    train_and_save()
