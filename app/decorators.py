# -*- coding: utf-8 -*-

from functools import wraps
from google.appengine.api import users
from webapp2 import cached_property


def requires_login(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            user = self.user
        except AttributeError:
            user = self.user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            return method(self, *args, **kwargs)

    return wrapper


def requires_admin(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not users.is_current_user_admin():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            return method(self, *args, **kwargs)

    return wrapper


