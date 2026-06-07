import json
import sys

import pandas as pd

from network_security.config.settings import get_settings
from network_security.db.mongodb import get_mongo_collection
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


class NetworkDataExtract:
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            return list(json.loads(data.T.to_json()).values())
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Backward-compatible alias for the original misspelled method.
    def cv_to_json_converter(self, file_path):
        return self.csv_to_json_converter(file_path=file_path)

    def insert_data_mongodb(self, records, database, collection):
        try:
            mongo_collection = get_mongo_collection(
                database_name=database,
                collection_name=collection,
                required=True,
            )
            if not records:
                logging.warning("No records provided for MongoDB insertion")
                return 0
            result = mongo_collection.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    settings = get_settings()
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(file_path=settings.paths.local_dataset_path)
    no_of_records = network_obj.insert_data_mongodb(
        records=records,
        database=settings.mongodb.database_name,
        collection=settings.mongodb.collection_name,
    )
    print(no_of_records)
