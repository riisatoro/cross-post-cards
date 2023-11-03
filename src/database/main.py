import os

import pymongo


MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DB = os.getenv('MONGO_DB_NAME')
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASS = os.getenv('MONGO_INITDB_ROOT_PASSWORD')


class Database:
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
