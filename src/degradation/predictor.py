"""
Degradation Predictor: Predicts State of Health (SoH) using XGBoost.
Your chemistry friend owns the electrochemical feature inputs here.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
from loguru import logger
import pickle
from pathlib import Path


class DegradationPredictor:
    """Predicts battery SoH from cycle features."""

    def __init__(self, model_path: str = "models/degradation_model.pkl"):
        self.model_path = Path(model_path)
        self.model = XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            random_state=42,
        )
        self.is_trained = False

    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """Train the degradation model. Returns evaluation metrics."""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.model.fit(X_train, y_train)
        self.is_trained = True
        preds = self.model.predict(X_test)
        metrics = {
            "mae": mean_absolute_error(y_test, preds),
            "r2": r2_score(y_test, preds),
        }
        logger.info(f"Model trained | MAE: {metrics['mae']:.3f} | R²: {metrics['r2']:.3f}")
        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict SoH (%) for given feature set."""
        if not self.is_trained:
            raise RuntimeError("Model not trained. Call train() or load() first.")
        return self.model.predict(X)

    def save(self):
        self.model_path.parent.mkdir(exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {self.model_path}")

    def load(self):
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        self.is_trained = True
        logger.info(f"Model loaded from {self.model_path}")
