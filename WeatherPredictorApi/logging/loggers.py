import logging

#https://docs.python.org/3/library/logging.html#logrecord-attributes

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

# fileHandler = logging.FileHandler('logs.log')
# fileHandler.setFormatter(formatter)

# streamHandler = logging.StreamHandler()  #to print to console, usually debug logs
# streamHandler.setFormatter(formatter)

# logger.addHandler(fileHandler)
# logger.addHandler(streamHandler)

import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime

class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def addFields(self, logRecord, record, messageDict):
        super(ElkJsonFormatter, self).add_fields(logRecord, record, messageDict)
        logRecord['@timestamp'] = datetime.now().isoformat()
        logRecord['level'] = record.levelname
        logRecord['logger'] = record.name

logging.config.fileConfig('./WeatherPredictorApi/logging/logging.conf')
logger = logging.getLogger('AppLogger')

logging.info('Application running!')