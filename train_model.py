import os

os.environ["MLFLOW_TRACKING_URI"] = "https://mlflow.staging.ml.usw2.upwork/"
os.environ["MLFLOW_TRACKING_URL"] = "https://mlflow.staging.ml.usw2.upwork/"
os.environ["SSL_CERT_FILE"] = "/tmp/upwork.pem"
os.environ["REQUESTS_CA_BUNDLE"] = "/tmp/upwork.pem"

import tempfile
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from umami.ml_core.experimentation.mlflow_tracker import MLFlowTracker, MLFlowTrackerConfig
from umami.ml_core.registrar.mlflow_registrar import MLflowRegistrar, MLFlowModelType

import boto3
import mlflow.store.artifact.s3_artifact_repo as s3_repo
s3_repo._get_s3_client = lambda *args, **kwargs: boto3.client('s3')

# TODO: things to improve in MlFlow managers
# Tracker
# - there is a bug where it doesnt end the correct run if i create it with start_run
# - use run as context
# - option to not create run right away w tracker
# - end run shouldnt use global mlflow context
# - why is use_artifact failing with error:
#   botocore.exceptions.PartialCredentialsError: Partial credentials found in explicit, missing: aws_secret_access_key 
#   the only way ive figured out how to fix this is to monkeypatch the s3_repo._get_s3_client function to use the my boto3 client
# Registrar
# - typo in registrar name: MLflowRegistrar -> MLFlowRegistrar

tracker = MLFlowTracker(
    MLFlowTrackerConfig(
        team_name="infra",
        project_name="model-serving-poc",
        user_email="ryanmelzer@upwork.com",
        experiment_group_name="MLI-4684",
    )
)

experiment_id = tracker.get_experiment_by_name("model-serving-poc").experiment_id
run_id = tracker.start_run(experiment_id=experiment_id)

random_state = 42
test_size = 0.5
model = XGBClassifier(random_state=random_state)
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

tracker.log_param("random_state", random_state)
tracker.log_param("test_size", test_size)
tracker.log_metric("accuracy", accuracy)
with tempfile.TemporaryDirectory() as temp_dir:
    model_path = Path(temp_dir) / "xgboost_model.json"
    model.save_model(model_path)
    tracker.log_artifact(str(model_path))
    print(f"Model saved and logged as MLFlow artifact: {model_path}")

tracker.end_run()

artifacts = tracker.client.list_artifacts(run_id)
print("Available artifacts:")
for artifact in artifacts:
    print(f"  - {artifact.path}")

downloaded_path = tracker.use_artifact("xgboost_model.json", local_path=".artifacts/", run_id=run_id)
print(f"Downloaded model to: {downloaded_path}")