from pymongo import MongoClient
import config
import data_cleaner
import json


class MongoService:

    def __init__(self, log_service):
        self.client = MongoClient(config.MONGO_IP,
                                  config.MONGO_PORT,
                                  username=config.MONGO_USER,
                                  password=config.MONGO_PASS)
        self.log_service = log_service

    def print_collection(self):
        try:
            print self.client.database_names()
        except Exception, e:
            self.log_service.log_error('Error occurred', e)
            return False

    def insert_data(self, data, collection_name, collection_keys):
        """
        Accepts a collection of raw data and then inserts this into the database
        :param data:
        :return:
        """
        try:
            self.log_service.log('Adding to database: {}'.format(collection_name))
            db = self.client[config.MONGO_DB_NAME][collection_name]
            curr_insert_record = None

            for row in data:
                try:
                    insert_record = {}
                    for field in collection_keys:
                        insert_record[field] = data_cleaner.clean_value(row[field])
                    # Clean data before inserting
                    insert_record = data_cleaner.clean_record(insert_record)
                    curr_insert_record = insert_record
                    self.insert_row(db, insert_record)
                except Exception, e:
                    self.log_service.log_error('INNER ERROR occurred in insert_data', e)
                    self.log_service.log('printing row:')
                    self.log_service.log(str(curr_insert_record))
        except Exception, e:
            self.log_service.log_error('Error occurred in insert_data', e)
            self.log_service.log('printing row:')
            self.log_service.log(str(curr_insert_record))
            return False

    def insert_row(self, db, record):
        """
        Inserts a record to database
        :param db:
        :param record:
        :return:
        """
        try:
            db.insert(record)
        except Exception, e:
            self.log_service.log_error('ERROR occurred in insert_row', e)
            self.log_service.log('printing row:')
            self.log_service.log(str(record))

    def delete_collection(self, collection_name):
        try:
            self.log_service.log('Deleting collection...{}'.format(collection_name))
            self.client[config.MONGO_DB_NAME].drop_collection(collection_name)
        except Exception, e:
            self.log_service.log_error('Error occurred in delete_collection', e)
            return False

