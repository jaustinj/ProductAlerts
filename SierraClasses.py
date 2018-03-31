import abc
import collections
import datetime
import logging
import re
import time

from bs4 import BeautifulSoup
import requests

class SierraProduct(Product):
        
    def _parse_html(self, tag):
        '''Parses values out of tag, one function for each
        value parsed'''
        
        @Product.log('Brand Parsed: {}')
        @Product.default_value('No Brand Found')
        def _brand(tag):
            return tag.find('a',
                           {'class': re.compile('^productCard-title.*')}
                           ).text.strip()
        
        @Product.log('Title Parsed: {}')
        @Product.default_value('No Title Found')
        def _title(tag):
            return tag.find('a',
                           {'class': re.compile('^display-block.*')}
                           ).text.strip()
        
        @Product.log('Price Parsed: {}')
        @Product.default_value(None)
        def _price(tag):
            price_str = tag.find('span', {'class': 'ourPrice'}).text.strip()
            return float(price_str.replace('$', ''))
        
        @Product.log('MSRP Parsed: {}')
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


class SierraPage(Page):
    
    def _select_product_class(self):
        return SierraProduct
    
    def _parse_html(self, tag):
        return tag.findAll('div', {'class': re.compile('^productThumbnailContainer.*')})


class SierraSearch(Search):
        
    def _search_url(self, search_string):
        '''Takes a search string and returns the url for
        the search on the website.
        
        Example:
        'oakley sunglasses' -> https://www.6pm.com/q?=oakley-sunglasses
        '''
        base_url = 'https://www.sierratradingpost.com/s~{}/'
        ammended_string = search_string.lower().replace(' ', '-')
        
        return base_url.format(ammended_string)
    
    def _select_page_class(self):
        '''Return the Page Class used to parse pages.
        i.e.: return MyPageParser'''
        return SierraPage
        
    def _find_next_page_url(self, soup):
        '''Given a search result page of html, find if there 
        is pagination (more results on other pages), and if so, return the 
        url of the next page, if not, return Null. Can also return a list
        of all urls in pagination.'''
        
        last_page = soup.findAll('a', 
                                 {'class': re.compile('^pageLink.*'), 
                                  'class': 'lastPage'}
                                )
        
        if last_page:
            href = last_page[0]['href']
            last_page_number = int(re.search('\d{1,3}', href).group())
            urls = [self.url + str(i) + '/' for i in range(2, last_page_number + 1)]
        
            return urls
        
        else:
            return None