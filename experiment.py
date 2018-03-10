import json
from pprint import pprint
import sys
import os
import config
from core.LogService import LogService
from core.DataFetch import DataFetch
from core.MongoService import MongoService

log_service = LogService(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs', config.LOG_FILE_NAME))

mongo = MongoService(log_service)
mongo.print_collection()

