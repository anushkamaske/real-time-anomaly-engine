import faust
import joblib
import numpy as np
from pydantic import BaseModel

KAFKA_BROKER = 'kafka://localhost:9092'
EVENT_TOPIC   = 'events'
ALERT_TOPIC   = 'anomalies'
MODEL_PATH    = 'models/anomaly_model.joblib'

app = faust.App('anomaly-detector', broker=KAFKA_BROKER)
model = joblib.load(MODEL_PATH)

class Event(BaseModel):
    timestamp: str
    sensor_id: int
    value: float

class Alert(BaseModel):
    timestamp: str
    sensor_id: int
    value: float
    score: float

event_topic = app.topic(EVENT_TOPIC,   value_type=Event)
alert_topic = app.topic(ALERT_TOPIC,   value_type=Alert)

@app.agent(event_topic)
async def detect(events):
    async for evt in events:
        features = np.array([[evt.sensor_id, evt.value]])
        score    = model.decision_function(features)[0]
        is_anom  = bool(model.predict(features)[0] == -1)
        if is_anom:
            await alert_topic.send(value=Alert(
                timestamp=evt.timestamp,
                sensor_id=evt.sensor_id,
                value=evt.value,
                score=score
            ))

if __name__ == '__main__':
    app.main()
