-- We need this file to create the database for the MLFlow auth db. If the database doesn't exist, MLFlow will throw an error.
SELECT 'CREATE DATABASE auth_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'auth_db')\gexec