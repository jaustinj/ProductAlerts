from time import sleep

from AlertClasses import *
from config import ALERT_CONFIG

while True:
  CheckSierra()
  CheckBackcountry()

  sleep(ALERT_CONFIG['TIME_BETWEEN_CHECKS'])


