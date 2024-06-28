class ModelTrainer:
    def __init__(self, input_dataset_path, input_features, target_feature, model_type, hyperparameters, output_model_path, test_size):
        self.input_dataset_path = input_dataset_path
        self.input_features = input_features
        self.target_feature = target_feature
        self.model_type = model_type
        self.hyperparameters = hyperparameters
        self.output_model_path = output_model_path
        self.model = None
        self.test_size = test_size

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

    def save_model(self):
        """Save the trained model to a file."""
        joblib.dump(self.model, self.output_model_path)

    def process(self):
        """Full processing pipeline."""
        self.load_data()
        self.train_model()
        self.save_model()