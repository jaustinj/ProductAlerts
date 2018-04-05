from ALertClasses import check_sierra

while True:
  check_sierra()

  time.sleep(ALERT_CONFIG['TIME_BETWEEN_CHECKS'])


