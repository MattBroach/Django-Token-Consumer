import requests

from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import resolve_url

from .models import Token
from .settings import token_settings

class APIHandler(object):
    def get(self, user, url, add_header=False):
        return self._api_call(user, url, 'get', add_header=add_header)

    def post(self, user, url, add_header=False, data={}):
        return self._api_call(user, url, 'post', add_header=add_header, data=data)

    def _api_call(self, user, url, method, add_header=False, data={}):
        """
        wrapper to make get calls to the target api
        """
        headers = self.get_headers(user) if add_header else {}

        response = getattr(requests, method)(token_settings.API_BASE_URL + url, headers=headers, data=data)

        return self.check_response(response)
    
    def get_headers(self, user):
        """
        Gets authentication headers for api calls
        if add_headers is set to True
        """
        try: 
            token = user.token.key
        except Token.DoesNotExist:
            return HttpResponseRedirect(resolve_url(settings.LOGIN_URL))

        headers = {token_settings.TOKEN_HEADER: token_settings.TOKEN_HEADER_PREFIX + token}
        return headers

    def check_response(self, response):
        """
        Checks that the response succeeded before returning data.
            - 404 will redirect to an improperly configued API page
            - 401 will logout the user and redirect to the login
            - 200s will return the parsed data
        """
        if response.status_code == 401:
            # TODO: implement expired token login redirect
            return HttpResponseRedirect(resolve_url(settings.LOGIN_URL))

        if response.status_code == 404:
            # TODO: implement missing 404 page
            print("404 Error!")
            pass

        if response.status_code >= 500:
            # TODO: implement server error page
            print("500+ Error!")
            pass

        return self.parse_data(response)
   
    def parse_data(self, response):
        """
        defines how successful data is parsed and returned
        """
        print(response.text)
        return response.json()
       

api = APIHandler()
