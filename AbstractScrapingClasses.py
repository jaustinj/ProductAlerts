import abc
import collections
import re

from bs4 import BeautifulSoup
import requests

class Product(collections.UserDict, abc.ABC):
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
       
    def default_value(default_value=None):
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
    
    @abc.abstractmethod
    def _parse_html(self, tag):
        '''Given a BeautifulSoup HTML tag, parse out the relevant
        information and return in a dict
        '''