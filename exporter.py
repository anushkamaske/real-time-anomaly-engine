from prometheus_client import start_http_server, Counter, Histogram
import time

anomaly_cnt = Counter('anomaly_count', 'Total anomalies detected')
latency_h   = Histogram('processing_latency_seconds', 'Stream processing latency')

if __name__ == '__main__':
    start_http_server(8001)
    print("Prometheus exporter listening on :8001")
    while True:
        # metrics are updated in your processor or tasks code
        time.sleep(1)
