import os
import logging

IGNORE = ('boxsdk', 'urllib3', 'universaldetector.close', 'charsetgroupprober.get_confidence',
          'sbcharsetprober.feed', 'eucjpprober.feed', 'sjisprober.feed')

fmt = '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s %(message)s'
for name in IGNORE:
    logging.getLogger(name).setLevel(logging.ERROR)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=LOG_LEVEL, format=fmt)
logger = logging.getLogger('learning')
logger.addHandler(logging.StreamHandler())
logger.setLevel(LOG_LEVEL)
