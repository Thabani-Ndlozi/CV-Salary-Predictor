import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "job_salary_prediction_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "salary_model.pkl")


def train_model():
    df = pd.read_csv(DATA_PATH)

    df = df.drop_duplicates()
    df = df.dropna()

    text_columns = [
        "job_title",
        "education_level",
        "industry",
        "company_size",
        "location",
        "remote_work",
    ]

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    df = df[
        (df["experience_years"] >= 0)
        & (df["experience_years"] <= 50)
        & (df["skills_count"] >= 0)
        & (df["certifications"] >= 0)
        & (df["salary"] > 0)
    ]

    X = df.drop("salary", axis=1)
    y = df["salary"]

    categorical_features = [
        "job_title",
        "education_level",
        "industry",
        "company_size",
        "location",
        "remote_work",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ],
        remainder="passthrough",
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Mean Absolute Error:", mae)
    print("R2 Score:", r2)

    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully at:", MODEL_PATH)


if __name__ == "__main__":
    train_model()