# MLflow and MinIO Subproject

This subproject is designed to manage machine learning model tracking and artifact storage using MLflow and MinIO, with PostgreSQL as the backend database.

## Overview

The server side of this project leverages Docker Compose to orchestrate MLflow, MinIO, and PostgreSQL. The client side requires configuration of environment variables to interact with the MLflow tracking server and MinIO for artifact storage.

## Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started) (for server setup)
- [Docker Compose](https://docs.docker.com/compose/install/) (for server setup)
- Python 3.x and pip (for client-side model training and MLflow interaction)

### .env Configuration

This project uses environment variables to manage sensitive information and configuration. Use the `.env.example` file as a template to create your own `.env` file.

#### 1. Server-Side Environment Variables

On the server side, you'll need to configure environment variables for MinIO, PostgreSQL, and MLflow. These should be defined in a `.env` file within the root directory.

```plaintext
# MinIO Configuration
MINIO_ROOT_USER=your_minio_root_user          # Replace with your MinIO root user (e.g., admin)
MINIO_ROOT_PASSWORD=your_minio_root_password  # Replace with your MinIO root password (e.g., password)
AWS_ACCESS_KEY_ID=your_aws_access_key         # Same as MINIO_ROOT_USER (for compatibility)
AWS_SECRET_ACCESS_KEY=your_aws_secret_key     # Same as MINIO_ROOT_PASSWORD (for compatibility)
S3_URL=http://s3:443                          # The MinIO endpoint URL; adjust to your setup
MLFLOW_BUCKET=your_mlflow_bucket              # S3 bucket for MLflow artifacts (e.g., mlflow)
DATASET_BUCKET=your_dataset_bucket            # S3 bucket for dataset storage (e.g., dataset)

# PostgreSQL Configuration
POSTGRES_USER=your_postgres_user              # PostgreSQL username (e.g., mlflow)
POSTGRES_PASSWORD=your_postgres_password      # PostgreSQL password (e.g., password)
POSTGRES_DB=your_postgres_db                  # PostgreSQL database name (e.g., mlflow)
PGADMIN_DEFAULT_EMAIL=your_pgadmin_email      # Email for pgAdmin (e.g., admin@example.com)
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password # Password for pgAdmin (e.g., password)
DB_URL=your_db_url                            # Database URL (e.g., db)
DB_ADMIN_URL=your_db_admin_url                # pgAdmin URL for administrative access

# Tracker (MLFlow) Configuration
MLFLOW_URL=your_mlflow_url                    # MLflow tracking server URL (e.g., http://localhost:5000)
TRACKER_URL=your_tracker_url                  # MLflow tracker URL (e.g., http://localhost:5000)
MLFLOW_ADMIN_USERNAME=your_mlflow_admin_username # MLflow admin username (e.g., admin)
MLFLOW_ADMIN_PASSWORD=your_mlflow_admin_password # MLflow admin password (e.g., password)
MLFLOW_AUTH_CONFIG_PATH=your_mlflow_auth_config_path # Path to MLflow auth config (e.g., /app/auth.ini)
```

#### 2. Client-Side Environment Variables

On the client side, you need to configure environment variables to interact with the MLflow server and MinIO. The client-side `.env` variables should also be filled in and stored locally for secure access when running client applications.

```plaintext
# Client Side Configuration

MLFLOW_S3_ENDPOINT_URL=your_mlflow_s3_endpoint_url # Endpoint URL for MinIO (e.g., http://localhost:9000 or http://localhost:443 if using SSL)
AWS_ACCESS_KEY_ID=your_aws_access_key              # Must match MINIO_ROOT_USER
AWS_SECRET_ACCESS_KEY=your_aws_secret_key          # Must match MINIO_ROOT_PASSWORD
MLFLOW_URL=your_mlflow_url                         # MLflow tracking server URL (same as above)
```

### Instructions

1. **Server-Side Setup**

   1. Clone the repository:
      ```bash
      git clone <repository-url>
      cd <project-directory>
      ```

   2. Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```

   3. Fill in the `.env` file with your actual configuration values for MinIO, PostgreSQL, and MLflow as described above.

   4. Run Docker Compose to start the services:
      ```bash
      docker-compose up --build
      ```

   The MLflow server, MinIO, and PostgreSQL will be running, and you can access the MLflow UI at `http://localhost:5000` (or the URL defined in `MLFLOW_URL`).

2. **Client-Side Setup**

   1. Copy `.env.example` to `.env` on the client side if it's a separate setup, or ensure the relevant client environment variables are available.

   2. Fill in the client-specific environment variables, ensuring `MLFLOW_S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `MLFLOW_URL` are correctly set.

   3. Install the required Python packages:
      ```bash
      pip install -r requirements.txt
      ```

   4. Run your model training and logging script:
      ```bash
      python code.py
      ```

## Accessing MLflow UI

- **MLflow Tracking Server**: Access the MLflow UI to track your experiments at the URL specified in `MLFLOW_URL` (e.g., `http://localhost:5000`).

## Important Notes

- **.env Security**: Ensure your `.env` file is not tracked in version control for security. Add `.env` to `.gitignore` if not already done.
- **MinIO Bucket Setup**: Run any setup scripts such as `prebucket.sh` to initialize MinIO buckets if required.

## Contact

For questions or issues, please contact:

- **Name**: Fauzan Ghaza Madani
- **Email**: contact@fauzanghaza.com
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/fauzanghaza/)
- **GitHub**: [Your GitHub Profile](https://github.com/ghazafm)