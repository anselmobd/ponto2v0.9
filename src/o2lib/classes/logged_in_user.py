from o2lib.classes.meta import SingletonMeta


class SingletonLoggedInUser(metaclass=SingletonMeta):
    __user = None

    def user_from_request(self, request):
        self.__user = request.user if request.user.is_authenticated else None

    @property
    def user(self):
        return self.__user
