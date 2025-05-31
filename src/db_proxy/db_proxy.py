import yaml
from src.db_proxy.mongodb import MongoDB


def load_config():
    with open("src/db_proxy/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def init_dbs():
    """
    Initialize the databases based on the loaded configuration.

    This function should be called to set up the database connections
    using the configuration loaded from the YAML file.
    """
    config = load_config()
    available_dbs = []
    for db in config.get("databases", []):
        # Initialize each database connection here
        db_name = db.get("name")
        db_type = db.get("type")
        connection_config = get_connection_config(config, db.get("connection"))
        if db_type == "mongodb":
            available_dbs.append(
                MongoDB(db_name, db_type, connection_config, db.get("collections", []))
            )
        else:
            print(f"Unsupported database type: {db_type}")
    if not available_dbs:
        print("No databases available. Please check your configuration.")
    return available_dbs


def get_connection_config(config, connection_name):
    for connection in config.get("connections", []):
        if connection.get("name") == connection_name:
            return connection


def get_db(name):
    """
    Retrieve a database connection by name.

    Args:
        name (str): The name of the database to retrieve.

    Returns:
        DB: The database connection object if found, otherwise None.
    """
    for db in available_dbs:
        if db.db_name == name:
            return db
    print(f"Database {name} not found.")
    return None


available_dbs = init_dbs()
