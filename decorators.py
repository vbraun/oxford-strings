# -*- coding: utf-8 -*-

from functools import wraps
from google.appengine.api import users


def requires_login(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            user = self.user
        except AttributeError:
            user = self.user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))
            return
        else:
            return method(self, *args, **kwargs)

    return wrapper


