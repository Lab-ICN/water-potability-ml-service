#!/bin/bash

# Start MinIO server in the background
minio server --address ":443" /data --console-address ":80" &

# Wait for MinIO server to be ready by checking connectivity
echo "Waiting for MinIO server to start..."
for i in {1..10}; do
  if mc alias set minio https://localhost:443 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}" --insecure &>/dev/null; then
    echo "MinIO server is ready."
    break
  else
    echo "MinIO server not ready, retrying in 2 seconds..."
    sleep 2
  fi
done

# Exit if MinIO is not ready after retries
if ! mc alias set minio https://localhost:443 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}" --insecure &>/dev/null; then
  echo "Error: MinIO server failed to start."
  exit 1
fi

# Create the 'mlflow' bucket if it doesn't exist
echo "Creating bucket 'mlflow' if it doesn't exist..."
if mc mb --ignore-existing --insecure minio/mlflow; then
  echo "Bucket 'mlflow' created or already exists."
else
  echo "Failed to create bucket 'mlflow'."
fi

# Create the 'dataset' bucket with versioning enabled if it doesn't exist
echo "Creating bucket 'dataset' with versioning enabled if it doesn't exist..."
if mc mb --with-versioning --ignore-existing --insecure minio/dataset; then
  echo "Bucket 'dataset' created with versioning or already exists."
else
  echo "Failed to create bucket 'dataset'."
fi

echo "Script completed successfully."

# Keep the script running
tail -f /dev/null