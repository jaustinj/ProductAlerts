from time import sleep

from AlertClasses import check_sierra
from config import ALERT_CONFIG

while True:
  check_sierra()

  sleep(ALERT_CONFIG['TIME_BETWEEN_CHECKS'])


