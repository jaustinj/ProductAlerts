import abc
import collections
import datetime
import functools
import logging
import re
import time

from bs4 import BeautifulSoup
import pandas as pd 
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from AlertingTools import *
from config import *


class CheckSite(abc.ABC):
  def __init__(self):
    self.config = self._set_config()
    self.Search = self._set_search()
    self.Htmlizer = self._set_htmlizer()
    self.main(self.config, self.Search, self.Htmlizer)

  @abc.abstractmethod
  def _set_config(self):
    '''return config for class
    e.g. return SIERRA_CONFIG
    '''

  @abc.abstractmethod
  def _set_search(self):
    '''return search class to use
    e.g. return SierraSearch
    '''

  @abc.abstractmethod
  def _set_htmlizer(self):
    '''return htmlizer to use
    e.g. return SierraHTMLizer
    '''

  def main(self, config, Search, Htmlizer):
    
    # Only most recent ts is pulled.  We'll attach
    # The same ts to all searches so they will all be pulled
    ts = datetime.datetime.now()

    for search in config['SEARCHES']:

        S = Search(search, 
          delay=config['DELAY_BETWEEN_PAGE_REQUESTS'])

        # send to postgres table with timestamp of this scrape
        S.to_postgres(config['POSTGRES_BASE_TABLE'], ts) 

    # Use SQL to find alerts from table that was just sent to posgres
    alerts_df = CheckDB(table=config['POSTGRES_BASE_TABLE'],
                        alert_table=config['POSTGRES_ALERT_TABLE'],
                        unique_sku=config['POSTGRES_SKU_COLUMN'],
                        threshold_column=config['THRESHOLD_COLUMN'],
                        threshold=config['THRESHOLD'],
                        eq=config['THRESHOLD_TYPE']).alerts


    if len(alerts_df) > 0:

        # Add some special formatting to the alerts and save as html file

        if config['SEARCH_EBAY_COLUMN']:
          alerts_df2 = add_ebay_link(alerts_df, config['SEARCH_EBAY_COLUMN'])
        else:
          alerts_df2 = alerts_df

        H = Htmlizer(alerts_df2)
        H.to_html('./alert_outputs/{}.html'.format(config['OUTPUT_FILE_NAME']))

        # Send email with html file output
        for email in EMAIL_CONFIG['SEND_TO']:
            send_alert(send_from=EMAIL_CONFIG['SEND_FROM'], 
                       send_to=email, 
                       username=EMAIL_CONFIG['USERNAME'], 
                       password=EMAIL_CONFIG['PASSWORD'],
                       subject=config['EMAIL_SUBJECT'], 
                       message='New Alerts, Download Below', 
                       file='./alert_outputs/{}.html'.format(config['OUTPUT_FILE_NAME']) 
                       )

        to_postgres(alerts_df, config['POSTGRES_ALERT_TABLE'])


# SIERRA TRADING POST ALERTS ==================================================


class CheckSierra(CheckSite):

  def _set_config(self):
    return SIERRA_CONFIG
    
  def _set_search(self):
    return SierraSearch

  def _set_htmlizer(self):
    return SierraHTMLizer


# BACKCOUNTRY ALERTS ==========================================================


class CheckBackcountry(CheckSite):

  def _set_config(self):
    return BACKCOUNTRY_CONFIG
    
  def _set_search(self):
    return BackcountrySearch

  def _set_htmlizer(self):
    return BackcountryHTMLizer







# def check_sierra():
#     for search in SIERRA_CONFIG['SEARCHES']:
#         S = SierraSearch(search, 
#                          delay=SIERRA_CONFIG['DELAY_BETWEEN_PAGE_REQUESTS'])
#         S.to_postgres('sierra_test_two') # send to posgres table 

#         # Uuse SQL to find alerts from table that was just sent to posgres
#         alerts_df = CheckDB(table='sierra_test_two',
#                             alert_table='sierra_test_two_alerted',
#                             unique_sku='title',
#                             threshold_column='perc_off',
#                             threshold=SIERRA_CONFIG['THRESHOLD'],
#                             eq='>=').alerts


#         if len(alerts_df) > 0:

#             # Add some special formatting to the alerts and save as html file
#             alerts_with_ebay = add_ebay_link(alerts_df, 'title')
#             SierraHTMLizer(alerts_with_ebay).to_html('./alert_outputs/sierra_alerts.html')

#             # Send email with html file output
#             for email in EMAIL_CONFIG['SEND_TO']:
#                 send_alert(send_from=EMAIL_CONFIG['SEND_FROM'], 
#                            send_to=email, 
#                            username=EMAIL_CONFIG['USERNAME'], 
#                            password=EMAIL_CONFIG['PASSWORD'],
#                            subject=EMAIL_CONFIG['SUBJECT'], 
#                            message='New Alerts, Download Below', 
#                            file='./alert_outputs/sierra_alerts.html' 
#                            )

#             to_postgres(alerts_df, 'sierra_test_two_alerted')


# # BACKCOUNTRY ALERTS ==========================================================
# def check_backcountry():
#     for search in BACKCOUNTRY_CONFIG['SEARCHES']:
#         S = SierraSearch(search, 
#                          delay=BACKCOUNTRY_CONFIG['DELAY_BETWEEN_PAGE_REQUESTS'])
#         S.to_postgres('sierra_test_two') # send to posgres table 

#     # Uuse SQL to find alerts from table that was just sent to posgres
#     alerts_df = CheckDB(table='backcountry_test',
#                         alert_table='backcountry_test_alerted',
#                         unique_sku='url',
#                         threshold_column='perc_off',
#                         threshold=BACKCOUNTRY_CONFIG['THRESHOLD'],
#                         eq='>=').alerts


#     if len(alerts_df) > 0:

#         # Add some special formatting to the alerts and save as html file
#         alerts_with_ebay = add_ebay_link(alerts_df, 'title')
#         SierraHTMLizer(alerts_with_ebay).to_html('./alert_outputs/backcountry_alerts.html')

#         # Send email with html file output
#         for email in EMAIL_CONFIG['SEND_TO']:
#             send_alert(send_from=EMAIL_CONFIG['SEND_FROM'], 
#                        send_to=email, 
#                        username=EMAIL_CONFIG['USERNAME'], 
#                        password=EMAIL_CONFIG['PASSWORD'],
#                        subject=EMAIL_CONFIG['SUBJECT'], 
#                        message='New Alerts, Download Below', 
#                        file='./alert_outputs/backcountry_alerts.html' 
#                        )

#         to_postgres(alerts_df, 'backcountry_test_alerted')

