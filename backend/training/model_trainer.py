from io import BytesIO
import joblib
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

class ModelTrainer:
    def __init__(self, input_dataset_uuid, training_params_uuid, db_handler):
        self.input_dataset_uuid = input_dataset_uuid
        self.training_params_uuid = training_params_uuid

        self.input_features = None
        self.target_feature = None
        self.model_type = None
        self.hyperparameters = None
        self.model = None
        self.test_size = None
        self.data = None
        self.db_handler = db_handler

    def load_data(self):
        """Load the training dataset from a CSV file."""
        self.data = self.db_handler.get_training_data(self.input_dataset_uuid)

    def load_training_params(self):
        """Load the training params."""
        results = self.db_handler.get_training_params(self.training_params_uuid)
        self.input_features = results.get("input_features", [])
        self.target_feature = results.get("target_feature", "")
        self.model_type = results.get("model_type", "")
        self.hyperparameters = results.get("hyperparameters", {})
        self.model = results.get("model", "")
        self.test_size = results.get("test_size", 0.2)

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

    def binarize_model(self):
        """Return the saved model as a binary format."""
        model_binary = BytesIO()
        joblib.dump(self.model, model_binary)
        model_binary.seek(0)
        return model_binary.read()
    
    def process(self):
        """Full processing pipeline."""
        self.load_data()
        self.load_training_params()
        self.train_model()
        model = self.binarize_model()
        self.db_handler.store_model(model, 'TEMPORARY_MUST_CHANGE')