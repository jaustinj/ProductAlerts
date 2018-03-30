import abc
import collections
import re

from bs4 import BeautifulSoup
import requests

class SierraProduct(Product):
        
    def _parse_html(self, tag):
        '''Parses values out of tag, one function for each
        value parsed'''
        
        @Product.default_value('No Brand Found')
        def _brand(tag):
            return tag.find('a',
                           {'class': re.compile('^productCard-title.*')}
                           ).text.strip()
        
        @Product.default_value('No Title Found')
        def _title(tag):
            return tag.find('a',
                           {'class': re.compile('^display-block.*')}
                           ).text.strip()
        
        @Product.default_value(None)
        def _price(tag):
            price_str = tag.find('span', {'class': 'ourPrice'}).text.strip()
            return float(price_str.replace('$', ''))
        
        @Product.default_value(None)
        def _msrp(tag):
            msrp_str = product_html.find('span', 
                                         {'class': re.compile('^retailPrice.*')}
                                        ).text.strip()
            msrp = re.search('\d{1,3}\.\d{2}', msrp_str).group()
            return float(msrp)
        
        data = {}
        
        data['brand'] = _brand(tag)
        data['title'] = _title(tag)
        data['price'] = _price(tag)
        data['msrp'] = _msrp(tag)
        
        return data
    