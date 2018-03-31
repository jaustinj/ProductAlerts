import abc
import collections
import datetime
import logging
import re
import time

from bs4 import BeautifulSoup
import requests

class ScraperMixIn(object):
    
    def default_value(default_value):
        '''Decorator that allows you to do quick try-excepts
        at parse time, and include a value if a result is Null'''
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except AttributeError:
                    return default_value
            return wrapper
        return decorator
    
    def log(logstring, log_level='debug'):
        def decorator(func):
            def wrapper(*args, **kwargs):
                ts = datetime.datetime.now()
                
                if log_level.lower() == 'debug':
                    result = func(*args, **kwargs)
                    logging.debug('{}: {}'.format(ts, logstring.format(result)))
                    
                elif log_level.lower() == 'info':
                    result = func(*args, **kwargs)
                    logging.info('{}: {}'.format(ts, logstring.format(result)))
                    
                elif log_level.lower() == 'warning':
                    result = func(*args, **kwargs)
                    logging.warning('{}: {}'.format(ts, logstring.format(result)))
                    
                elif log_level.lower() == 'error':
                    result = func(*args, **kwargs)
                    logging.error('{}: {}'.format(ts, logstring.format(result)))
                    
                elif log_level.lower() == 'critical':
                    result = func(*args, **kwargs)
                    logging.critical('{}: {}'.format(ts, logstring.format(result)))
                    
                else:
                    result = func(*args, **kwargs)
                    logging.debug(
                        '{}: NO-LEVEL-CHOSEN {}'.format(ts, logstring.format(result))
                        )
                
                return result
            return wrapper
        return decorator

class Product(collections.UserDict, abc.ABC, ScraperMixIn):
	'''Given a BeautifulSoup htmlTag, this class will
	parse the tag and return a dictionary object 
	containing the parsed information

	The user must define _parse_html, which parses the 
	tag and returns a dictionary of the parsed attributes.

	The @Product.default_value() decorator can be used in 
	any child class inside _parse_html in order to provide 
	easier try-except catches and value defaulting when
	no value is found.
	'''
    def __init__(self, htmlTag):
    	'''collections.UserDict requires a dictionary object
    	called self.data.  _parse_html returns
    	a dictionary object to self.data, which then allows
    	the object to be used as a normal dictionary object
    	'''

        self.data = self._parse_html(htmlTag)
    
    @abc.abstractmethod
    def _parse_html(self, tag):
        '''Given a BeautifulSoup HTML tag, parse out the relevant
        information and return in a dict
        '''

class Page(collections.UserList, abc.ABC):
    def __init__(self, htmlTag):
        self.page_html = htmlTag
        self.product_htmls = self._parse_html(htmlTag)
        self.ProductClass = self._select_product_class()
        self.data = self._html2Products(self.product_htmls)
    
    @abc.abstractmethod
    def _select_product_class(self):
        '''Return the Product Class used to parse products on page.
        i.e.: return MyProductParser'''
        
    @abc.abstractmethod
    def _parse_html(self, tag):
        '''Given a BeautifulSoup HTML tag, return list
        of HTML tags that contain all product information
        to be parsed by Product Class
        '''
    
    def _html2Products(self, list_of_product_tags):
        return [self.ProductClass(product) for product in list_of_product_tags]


class Search(collections.UserList, abc.ABC, ScraperMixIn):
    def __init__(self, search_string, delay=1):
        self.url = self._search_url(search_string)
        self.PageClass = self._select_page_class()
        self.data, self.page_results = self._main(search_string)
     
    
    @abc.abstractmethod
    def _select_page_class(self):
        '''Return the Page Class used to parse pages.
        i.e.: return MyPageParser'''
        
    @abc.abstractmethod
    def _search_url(self, search_string):
        '''Takes a search string and returns the url for
        the search on the website.
        
        Example:
        'oakley sunglasses' -> https://www.6pm.com/q?=oakley-sunglasses
        '''
        
    @ScraperMixIn.log('Scraping New Page', 'debug')
    def _soupify(self, search_url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        c = requests.get(search_url, headers=headers).content
        time.sleep(delay)
        return BeautifulSoup(c, 'html5lib')
        
    @abc.abstractmethod
    def _find_next_page_url(self, soup):
        '''Given a search result page of html, find if there 
        is pagination (more results on other pages), and if so, return the 
        url of the next page, if not, return Null. Can also return a list
        of all urls in pagination.'''
    
    def _create_list_of_page_soups(self, soup):
        urls = [soup]
        
        pagination = self._find_next_page_url(soup)
        if pagination:
            if isinstance(pagination, list):
                pagination_soups = [self._soupify(p) for p in pagination]
                urls += pagination_soups
                
            elif isinstance(pagination, str):
                while pagination:
                    next_soup = self._soupify(pagination)
                    urls.append(next_soup)
                    pagination = self._find_next_page_url(next_soup)
            
        return urls
        
    def _html2Pages(self, list_of_page_soups):
        raw = [self.PageClass(page) for page in list_of_page_soups]
        lol = [list(self.PageClass(page)) for page in list_of_page_soups]
        return (raw, lol)
    
    def _main(self, search):
        search_url = self.url
        search_landing_soup = self._soupify(search_url)
        list_of_page_soups = self._create_list_of_page_soups(search_landing_soup)
        raw_pages, list_of_lists = self._html2Pages(list_of_page_soups)
        flattened_products = [val for sublist in list_of_lists for val in sublist]
        
        return (flattened_products, raw_pages)