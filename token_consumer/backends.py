import requests

from django.conf import settings
from django.contrib.auth import get_user_model

from .settings import token_settings
from .models import Token

User = get_user_model()

class TokenConsumerBackend(object):
    """
    User an external token-based login system for django authentication.
    Will maintain login locally and with remote server, and decorate the api calls 
    with the appropriate header
    """

    def authenticate(self, username=None, password=None):
        # Ask the token provider for login
        endpoints = token_settings.AUTH_ENDPOINTS
        base = token_settings.API_BASE_URL
        response = requests.post(base+endpoints['LOGIN'], data={
            'username': username,
            'password': password
        })

        if response.status_code == 200:
            """
            status code 200 means login was successful.
            Get or create the requisite user and token models
            """
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, password="Password Not Stored")
                user.save()

            data = response.json()

            try:
                user.token.key = data['key']
            except Token.DoesNotExist:
                token = Token(key=data['key'], user=user)
                token.save()

            return user

        return None

     
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
