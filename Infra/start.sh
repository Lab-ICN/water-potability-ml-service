#!/bin/sh

# Export required environment variables
export MLFLOW_S3_ENDPOINT_URL=$MLFLOW_S3_ENDPOINT_URL
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export MLFLOW_DEBUG=true
export MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING=true

echo "Environment Variables for Debugging:"
echo "------------------------------------"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "POSTGRES_URL: $DB_URL"
echo "S3_URL: $MLFLOW_S3_ENDPOINT_URL"
echo "MLFLOW_BUCKET: $MLFLOW_BUCKET"
echo "AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
echo "AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
echo "TLS: $MLFLOW_S3_IGNORE_TLS"
echo "username: $MLFLOW_TRACKING_USERNAME"
echo "pass: $MLFLOW_TRACKING_PASSWORD"
echo "------------------------------------"

python /root/mlflow/auth/ini_script.py

# Run mlflow server with necessary environment variables
mlflow server \
  --app-name basic-auth \
  --backend-store-uri "postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_URL}/${POSTGRES_DB}" \
  --host "0.0.0.0" \
  --port "5000" \
  --serve-artifacts \
  --default-artifact-root "s3://${MLFLOW_BUCKET}"
