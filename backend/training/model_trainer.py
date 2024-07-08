from io import BytesIO
import joblib
import psycopg2
import pandas as pd
from sklearn.base import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

class ModelTrainer:
    def __init__(self, input_dataset_path, input_features, target_feature, model_type, 
                 hyperparameters, output_model_path, test_size, db_params):
        self.input_dataset_path = input_dataset_path
        self.input_features = input_features
        self.target_feature = target_feature
        self.model_type = model_type
        self.hyperparameters = hyperparameters
        self.output_model_path = output_model_path
        self.model = None
        self.test_size = test_size
        self.db_params = db_params

    def load_data(self):
        """Load the training dataset from a CSV file."""
        self.data = pd.read_csv(self.input_dataset_path)

    def train_model(self):
        """Train a Decision Tree model."""
        X = self.data[self.input_features]
        y = self.data[self.target_feature]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)

        if self.model_type == 'DecisionTreeClassifier':
            self.model = DecisionTreeClassifier(**self.hyperparameters)
        elif self.model_type == 'DecisionTreeRegressor':
            self.model = DecisionTreeRegressor(**self.hyperparameters)
        else:
            raise ValueError("Invalid model_type.")

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        if self.model_type == 'DecisionTreeClassifier':
            self.score = accuracy_score(y_test, y_pred)
        elif self.model_type == 'DecisionTreeRegressor':
            self.score = mean_squared_error(y_test, y_pred)

        print(f"Model performance: {self.score}")

    def export_model(self):
        """Return the saved model as a binary format."""
        model_binary = BytesIO()
        joblib.dump(self.model, model_binary)
        model_binary.seek(0)
        return model_binary.read()
    
    def store_model_in_db(model_binary, model_name, conn_params):
        """Store the binary model data in the database."""
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO models (name, model_data) VALUES (%s, %s)",
            (model_name, psycopg2.Binary(model_binary))
        )
        conn.commit()
        cur.close()
        conn.close()

    def process(self):
        """Full processing pipeline."""
        self.load_data()
        self.train_model()
        model = self.export_model()
        self.store_model_in_db(model, 'TEMPORARY_MUST_CHANGE', self.db_params)