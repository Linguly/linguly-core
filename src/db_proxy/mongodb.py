from src.db_proxy.db import DB
import pymongo
import sys
import os


class MongoDB(DB):
    def __init__(
        self,
        db_name: str,
        db_type: str = "mongodb",
        connection_config: dict = None,
        collections: list = None,
    ):
        super().__init__(db_type)
        self.db_name = db_name
        self.connection_config = connection_config if connection_config else {}
        self.collections = collections if collections else []
        self.db = None
        self.connect()

    def connect(self):
        uri = os.getenv(self.connection_config.get("url_env_var"), "")
        try:
            client = pymongo.MongoClient(uri)

        # return a friendly error if a URI error is thrown
        except pymongo.errors.ConfigurationError:
            print(
                "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
            )
            sys.exit(1)

        print(f"Connected to database: {self.db_name}, type: {self.db_type}")
        self.db = client[self.db_name]

    def disconnect(self):
        if self.client:
            self.client.close()
            print(f"Disconnected from database: {self.db_name}")

    def find(self, collection: str, query: dict) -> list:
        """Find documents in a specified collection based on a query.
        Args:
            collection (str): The name of the collection to search.
            query (dict): The query to filter documents.
        Returns:
            list: A list of documents matching the query.
        Raises:
            ValueError: If the collection does not exist in the database.
        """
        if collection not in self.collections:
            raise ValueError(
                f"Collection {collection} not found in database {self.db_name}"
            )
        return list(self.db[collection].find(query))

    def insert(self, collection: str, document: dict) -> str:
        """Insert a document into a specified collection.
        Args:
            collection (str): The name of the collection to insert into.
            document (dict): The document to insert.
        Returns:
            str: The ID of the inserted document.
        Raises:
            ValueError: If the collection does not exist in the database.
        """
        if collection not in self.collections:
            raise ValueError(
                f"Collection {collection} not found in database {self.db_name}"
            )
        result = self.db[collection].insert_one(document)
        return str(result.inserted_id)

    def update(self, collection: str, query: dict, update: dict) -> int:
        """Update documents in a specified collection based on a query.
        Args:
            collection (str): The name of the collection to update.
            query (dict): The query to filter documents to update.
            update (dict): The update operation to apply.
        Returns:
            int: The number of documents updated.
        Raises:
            ValueError: If the collection does not exist in the database.
        """
        if collection not in self.collections:
            raise ValueError(
                f"Collection {collection} not found in database {self.db_name}"
            )
        result = self.db[collection].update_many(query, update)
        return result.modified_count

    def delete(self, collection: str, query: dict) -> int:
        """Delete documents in a specified collection based on a query.
        Args:
            collection (str): The name of the collection to delete from.
            query (dict): The query to filter documents to delete.
        Returns:
            int: The number of documents deleted.
        Raises:
            ValueError: If the collection does not exist in the database.
        """
        if collection not in self.collections:
            raise ValueError(
                f"Collection {collection} not found in database {self.db_name}"
            )
        result = self.db[collection].delete_many(query)
        return result.deleted_count
