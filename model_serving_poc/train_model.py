from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from umami.ml_core.experimentation.mlflow_tracker import MLFlowTracker

 
model = XGBClassifier(random_state=42)

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.3f}")

# TODO: create experiment
# TODO: create run
# TODO: log params
# TODO: log metrics
# TODO: log model
# TODO: register model
