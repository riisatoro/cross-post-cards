import os

import pymongo

from authorization.passwords import make_password


MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DB = os.getenv('MONGO_DB_NAME')
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASS = os.getenv('MONGO_INITDB_ROOT_PASSWORD')


class Database:
    USER_COLLECTION_NAME = 'users'

    client = pymongo.MongoClient(
        host=MONGO_HOST,
        port=int(MONGO_PORT),
        username=MONGO_USER,
        password=MONGO_PASS,
    )
    db = client[MONGO_DB]

    @staticmethod
    def health_check():
        """Checks availability of the database."""
        return Database.client.admin.command('ping')

    @staticmethod
    def create_user(user):
        """Creates a new user."""
        user.password = make_password(user.password)
        Database.db[Database.USER_COLLECTION_NAME].insert_one(user.dict())

    @staticmethod
    def get(collection: str, query: dict):
        """Gets a document from the database."""
        return Database.db[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: dict, data: dict):
        """Updates a document in the database."""
        return Database.db[collection].update_one(query, {'$set': data})