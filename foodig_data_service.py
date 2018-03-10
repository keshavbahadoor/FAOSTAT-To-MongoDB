import sys
import os
import config
from core.LogService import LogService
from core.DataFetch import DataFetch
from core.MongoService import MongoService

# Create log service object for global use.
log_service = LogService(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs', config.LOG_FILE_NAME))
data_importer = DataFetch(log_service)


def test_database_connection():
    mongo = MongoService(log_service)
    mongo.print_collection()


def main_process():
    if sys.argv.__len__() == 1:
        log_service.log('No arguments passed..')
    else:
        log_service.log('Argument passed: {}'.format(sys.argv[1]))
        if sys.argv[1] == 'test db':
            test_database_connection()
        if sys.argv[1] == 'import_data':
            data_importer.import_data()

main_process()
