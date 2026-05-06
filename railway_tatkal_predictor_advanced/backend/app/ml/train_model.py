
from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.ml.predictor import FEATURE_COLUMNS

DATA_PATH = Path("data/sample_history.csv")
ARTIFACT_DIR = Path("app/ml/artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_COLUMNS]
    y = df["final_status"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    rf = RandomForestClassifier(n_estimators=160, max_depth=8, random_state=42, class_weight="balanced")
    gb = GradientBoostingClassifier(random_state=42)
    model = VotingClassifier(estimators=[("rf", rf), ("gb", gb)], voting="soft")
    model.fit(X_train, y_train)
    print(classification_report(y_test, model.predict(X_test)))
    joblib.dump(model, ARTIFACT_DIR / "tatkal_model.joblib")
    print("Saved model to", ARTIFACT_DIR / "tatkal_model.joblib")
