-- Drop tables if they already exist to ensure a clean slate
DROP TABLE IF EXISTS deployables CASCADE;
DROP TABLE IF EXISTS models CASCADE;
DROP TABLE IF EXISTS datasets CASCADE;
DROP TABLE IF EXISTS training_params CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  company_name VARCHAR(100),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  auth_id VARCHAR(100) NOT NULL UNIQUE
);

CREATE INDEX idx_users_auth_id ON users(auth_id);

-- Create projects table
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description VARCHAR(500),
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user_id ON projects(user_id);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON projects
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Create training_params table
CREATE TABLE training_params (
  id SERIAL PRIMARY KEY,
  params JSON NOT NULL,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_training_params_project_id ON training_params(project_id);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON training_params
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Create datasets table
CREATE TABLE datasets (
  uuid UUID PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  size INTEGER NOT NULL CHECK (size >= 0),
  name VARCHAR(100) NOT NULL,
  data BYTEA NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_datasets_project_id ON datasets(project_id);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON datasets
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Create models table
CREATE TABLE models (
  uuid UUID PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  data BYTEA NOT NULL,
  dataset_id UUID NOT NULL REFERENCES datasets(uuid) ON DELETE CASCADE,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_models_project_id ON models(project_id);
CREATE INDEX idx_models_dataset_id ON models(dataset_id);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON models
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Create deployables table
CREATE TABLE deployables (
  uuid UUID PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  params_id INTEGER NOT NULL REFERENCES training_params(id) ON DELETE CASCADE,
  model_id UUID NOT NULL REFERENCES models(uuid) ON DELETE CASCADE,
  dataset_id UUID NOT NULL REFERENCES datasets(uuid) ON DELETE CASCADE,
  data BYTEA NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_deployables_project_id ON deployables(project_id);
CREATE INDEX idx_deployables_params_id ON deployables(params_id);
CREATE INDEX idx_deployables_model_id ON deployables(model_id);
CREATE INDEX idx_deployables_dataset_id ON deployables(dataset_id);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON deployables
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();