# -*- coding: utf-8 -*-
"""
Data model for editable pages
"""

from google.appengine.ext import ndb


default_source = """
Sections:

Section
=======

Subsection
-------

Alternative syntax for sections:

# Section
## Subsection
### Subsubsection

Paragraphs:

Paragraphs of text are separated by an empty line, just as in
TeX. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Lorem
ipsum dolor sit amet, consectetuer adipiscing elit.

Separate paragraph. Lorem ipsum dolor sit amet, consectetuer
adipiscing elit. Lorem ipsum dolor sit amet, consectetuer adipiscing
elit.

Itemized lists: 

*   Red
*   Green
*   Blue
*   This is a list item with two paragraphs.

    This is the second paragraph in the list item. You're only
required to indent the first line. Lorem ipsum dolor sit amet,
consectetuer adipiscing elit.

*   Another item in the same list.

Enumerated lists: 

1.  first
1.  second
1.  third

Horizontal line:

- - -

Tables:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

Inline HTML:

<i>italics</i>, <b>bold</b>, <tt>typewriter</tt>
"""





class Page(ndb.Model):
    """
    A page with editable content
    """
    date = ndb.DateTimeProperty(auto_now_add=True)
    user = ndb.StringProperty(required=False, indexed=False)
    source = ndb.TextProperty()

    
    @classmethod
    def make_key(cls, name):
        return ndb.Key(cls, name)

    @classmethod
    def query_name(cls, name):
        key = cls.make_key(name)
        return cls.query(ancestor=key).order(-cls.date)

    @classmethod
    def create(cls, name, source, user=None):
        key = cls.make_key(name)
        args = dict()
        args['parent'] = key
        args['source'] = source
        if user:
            args['user'] = user
        page = Page(**args)
        page.put()
        return page

    @classmethod
    def load(cls, name):
        pages = cls.query_name(name).fetch(1)
        if len(pages) == 0:
            return cls.create(name, default_source)
        else:
            return pages[0]
            

