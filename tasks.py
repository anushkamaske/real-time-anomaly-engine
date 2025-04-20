import os
from celery import Celery
from slack_sdk import WebClient

CELERY_BROKER = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
SLACK_TOKEN   = os.getenv('SLACK_TOKEN')

app   = Celery('tasks', broker=CELERY_BROKER)
slack = WebClient(token=SLACK_TOKEN)

@app.task
def send_alert(alert: dict):
    text = (
        f"🚨 *Anomaly Detected*\n"
        f"> Sensor: {alert['sensor_id']}\n"
        f"> Value: {alert['value']}\n"
        f"> Score: {alert['score']}"
    )
    slack.chat_postMessage(channel='#alerts', text=text)
