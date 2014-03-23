"""
Menu items
"""


class MenuItem(object):
    
    def __init__(self, name, url=None, level=0):
        self._name = name
        self._url = url
        self._level = level

    def get_name(self):
        return self._name
        
    def get_url(self):
        return self._url

    def get_css(self):
        return 'menu_lvl_'+str(self._level)
        


menu_items = (
    MenuItem('Home', 'index.html'),
    MenuItem('Members', 'members.html'),
    MenuItem('Research', 'index.html'),
    MenuItem('Seminars', 'seminars.html'),
    MenuItem('Bag lunch', 'bag_lunch.html', 1),
    MenuItem('This week', 'thisweek.html', 1),
    MenuItem('Graduate study', 'graduates.html'),
)
    
