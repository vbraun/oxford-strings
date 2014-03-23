



class User(object):

    def __init__(self, name):
        self._name = name

    @property
    def is_anonymous(self):
        return False


class UserAnonymous(User):

    def __init__(self):
        pass

    @property
    def is_anonymous(self):
        return False


anonymous = UserAnonymous()
    
