from fastapi import FastAPI, HTTPException
from pydantic  import BaseModel
import requests
import os

app = FastAPI()
BENTO_URL = os.getenv('BENTO_URL', 'http://bento_service:5000/predict')

class Event(BaseModel):
    timestamp: str
    sensor_id: int
    value: float

class Feedback(BaseModel):
    id: str
    label: bool

@app.post('/predict')
def predict(evt: Event):
    resp = requests.post(BENTO_URL, json=evt.dict())
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()

@app.post('/feedback')
def feedback(fb: Feedback):
    # TODO: store feedback in a DB or push to MLflow for retraining
    return {'status': 'received'}
