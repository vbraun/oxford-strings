"""
Menu items
"""


import logging


class MenuItem(object):
    
    def __init__(self, name, url=None, level=0):
        self._name = name
        self._url = url
        self._level = level
        if not url.startswith('/'):
            logging.warn('url must start with slash, got ' + url)

    def get_name(self):
        return self._name
        
    def get_url(self):
        return self._url

    def get_css(self, page_url):
        if page_url == self._url:
            return 'menu_selected menu_lvl_'+str(self._level)
        else:
            return 'menu_lvl_'+str(self._level)
        

    
