"""
Settings for the token_consumer application.

provides the token_settings object for accessing the settings, which checks the project
settings before falling back to defaults.

This settings file is heavily indebted to that of Django Rest Framework:
http://www.django-rest-framework.org/
"""

from django.conf import settings
from django.test.signals import setting_changed


DEFAULTS = {
    'API_BASE_URL': '',
    'TOKEN_HEADER_PREFIX': 'Token ',
    'TOKEN_HEADER': 'Authorization',
    'AUTH_ENDPOINTS': {
        'LOGIN': '',
        'LOGOUT': '',
        'SIGNUP': ''
    },
}


class TokenSettings(object):
    """
    class based settings object.  Accessed as: 
        token_settings.PROPERTY
    """

    def __init__(self, project_settings=None):
        self.defaults = DEFAULTS
        self.project_settings = project_settings if project_settings else getattr(settings, 'TOKEN_CONSUMER', {})

        if (not self.project_settings.get('AUTH_ENDPOINTS', {}).get('LOGIN', None) or 
            not self.project_settings.get('AUTH_ENDPOINTS', {}).get('LOGOUT', None)):
                msg = ("You MUST set the 'LOGIN' and 'LOGOUT' values" 
                       "of the TOKEN_SETTINGS['AUTH_ENDPOINTS']"
                       "in your settings file")
                raise AttributeError(msg)

        if not self.project_settings.get('API_BASE_URL', None):
                msg = ("You MUST set the TOKEN_SETTINGS['API_BASE_URL']"
                       "value in your settings file")
                raise AttributeError(msg)

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Token Consumer setting: '{}'".format(attr))

        try:
            # Get project specific version
            val = self.project_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


token_settings = TokenSettings(None)


def reload_token_settings(*args, **kwargs):
    global token_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'TOKEN_CONSUMER':
        token_settings = TokenSettings(value)


setting_changed.connect(reload_token_settings)
