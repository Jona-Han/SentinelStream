class Packager:
    def __init__(self, model_uuid, db_handler):
        self.model_uuid = model_uuid
        self.model = None

        self.db_handler = db_handler

    def load_model_from_db(self):
        """Loads the model from the db"""
        self.model = self.db_handler.get_model(self.model_uid)

    def build_deployable(self):
        """Builds the containerized application"""
        
    
