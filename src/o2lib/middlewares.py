from pprint import pprint

from o2lib.classes.logged_in_user import SingletonLoggedInUser


class LoggedInUserMiddleware:
    '''
        Insert this middleware after
        django.contrib.auth.middleware.AuthenticationMiddleware
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        logged_in_user = SingletonLoggedInUser()
        logged_in_user.user_from_request(request)

        return response
