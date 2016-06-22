import requests

from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import resolve_url

from .models import Token
from .settings import token_settings

class APIHandler(object):
    def get(self, url, user=None):
        return self._api_call(url, 'get', user=user)

    def post(self, url, user=None, data={}):
        return self._api_call(url, 'post', user=user, data=data)

    def _api_call(self, url, method, user=None, data={}):
        """
        wrapper to make get calls to the target api
        """
        headers = self.get_headers(user) if user else {}

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
            return HttpResponseRedirect(resolve_url(settings.LOGIN_URL))

        if response.status_code == 404:
            raise Http404(
                "The API Endpoint accessed does not exist. "
                "Please make sure that {} is the intended endpoint"
                "".format(response.url)
            )

        if response.status_code == 403:
            # TODO: implement forbidden view
            print("403 Error")
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
        return response.json()
       

api = APIHandler()
