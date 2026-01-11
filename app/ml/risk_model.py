import numpy as np
from sklearn.linear_model import LogisticRegression


class RiskPredictionModel:
    def __init__(self):
        self.model = LogisticRegression()
        self.is_trained = False

    def train(self, X, y):
        """
        X: list of feature vectors
        y: binary labels (0 = safe, 1 = at risk)
        """
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, features):
        """
        Returns:
        - probability
        - confidence
        """
        if not self.is_trained:
            raise RuntimeError("Risk model not trained")

        prob = self.model.predict_proba([features])[0][1]
        confidence = max(prob, 1 - prob)

        return prob, confidence
