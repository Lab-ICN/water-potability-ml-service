import os
import configparser
import time


def create_ini_file(config_file_path):
    # Check if the configuration file exists
    if not os.path.exists(config_file_path):
        print(
            f"Configuration file does not exist. Creating new file: {config_file_path}"
        )
        # Create a new config file if it does not exist
        with open(config_file_path, "w") as configfile:
            configfile.write("[mlflow]\n")  # Start with a basic [mlflow] section
        print(f"New config file created at {config_file_path}")

    # Proceed to modify the ini file
    modify_ini_file(config_file_path)


def modify_ini_file(config_file_path):
    # Create a ConfigParser instance
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(config_file_path)

    # Ensure the 'mlflow' section exists, or create it
    if "mlflow" not in config.sections():
        config.add_section("mlflow")
        print("Created new section [mlflow]")

    # Get environment variables or default to empty string if not found
    postgres_user = os.getenv("POSTGRES_USER", "")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "")
    db_url = os.getenv("DB_URL", "")
    postgres_db = os.getenv("POSTGRES_DB", "")
    mlflow_tracking_username = os.getenv("MLFLOW_TRACKING_USERNAME", "")
    mlflow_tracking_password = os.getenv("MLFLOW_TRACKING_PASSWORD", "")

    # Modify configuration values
    config.set("mlflow", "default_permission", "READ")

    # Modify the database_uri option using the environment variables
    database_uri = (
        f"postgresql://{postgres_user}:{postgres_password}@{db_url}:5432/auth_db"
    )
    config.set("mlflow", "database_uri", database_uri)

    # Modify admin username and password options
    config.set("mlflow", "admin_username", mlflow_tracking_username)
    config.set("mlflow", "admin_password", mlflow_tracking_password)

    config.set(
        "mlflow",
        "authorization_function",
        "mlflow.server.auth:authenticate_request_basic_auth",
    )

    # Save the modified config back to the file
    with open(config_file_path, "w") as configfile:
        config.write(configfile)

    print(f"Configuration updated successfully: {config_file_path}")


if __name__ == "__main__":
    # Path to your config file
    config_file_path = "/root/mlflow/auth/basic_auth.ini"

    # Create and modify the config file
    create_ini_file(config_file_path)