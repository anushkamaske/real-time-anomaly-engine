import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer

KAFKA_BROKER = 'localhost:9092'
TOPIC = 'events'

def delivery_report(err, msg):
    if err:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def generate_event():
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'sensor_id': random.randint(1, 5),
        'value': random.uniform(0, 100)
    }

def main():
    p = Producer({'bootstrap.servers': KAFKA_BROKER})
    while True:
        event = generate_event()
        p.produce(TOPIC, json.dumps(event).encode('utf-8'), callback=delivery_report)
        p.poll(0)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
