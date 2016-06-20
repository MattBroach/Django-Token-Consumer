import requests

from django.conf import settings
from django.contrib.auth import get_user_model

from .settings import token_settings

User = get_user_model()


class TokenConsumerBackend(object):
    """
    User an external token-based login system for django authentication.
    Will maintain login locally and with remote server, and decorate the api calls 
    with the appropriate header
    """

    def authenticate(self, username=None, password=None):
        pass


