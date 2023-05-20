import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

class Model:
    def __init__(self, df: pd.DataFrame, target: str, model, test_size: float = 0.2):
        """
        Model class. Takes dataframe and target column name, takes model instance class to train it 
        on the data and use it for inference.
        """
        self.X = df.drop(target, axis = 1)
        self.y = df[target]
        self.model = model
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=test_size, random_state=420)
    
    def fit_model(self):
        self.model.fit(self.X_train, self.y_train)
    
    def predict(self, X_test = None):
        if not X_test:
            return self.model.predict(self.X_test)
        else:
            return self.model.predict(X_test)
    def evaluate(self, X = None, y = None):
        if not X:
            y_pred = self.model.predict(self.X_test)
            y = self.y_test    
        else: 
            y_pred = self.model.predict(X)
        f1 = f1_score(y, y_pred)
        accuracy = accuracy_score(y, y_pred)
        return f1, accuracy

