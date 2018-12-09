import json
import logging
import warnings

#logging.warning('Watch out!')  # will print a message to the console
#logging.info('I told you so')  # will not print anything

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

