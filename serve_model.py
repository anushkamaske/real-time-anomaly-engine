import bentoml
from bentoml.io import JSON
import joblib
import numpy as np

MODEL_PATH = 'models/anomaly_model.joblib'
model = joblib.load(MODEL_PATH)

@bentoml.env(infer_pip_packages=True)
@bentoml.artifacts([bentoml.artifact.PickleArtifact('model')])
class AnomalyService(bentoml.BentoService):

    @bentoml.api(input=JSON(), output=JSON())
    def predict(self, parsed):
        features   = np.array([[parsed['sensor_id'], parsed['value']]])
        score      = self.artifacts.model.decision_function(features)[0]
        anomaly    = int(self.artifacts.model.predict(features)[0]) == -1
        return {'score': score, 'anomaly': anomaly}

if __name__ == '__main__':
    svc = AnomalyService().pack('model', model)
    svc.save()
