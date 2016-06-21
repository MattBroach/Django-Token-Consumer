from django.views.decorators.cache import never_cache
from django.contrib.auth.views import logout

from .handlers import api
from .settings import token_settings

def token_logout(request, template_name="token_consumer/logout.html"):
    api.post(request.user, 
             token_settings.AUTH_ENDPOINTS['LOGOUT'],
             add_header=True)

    return logout(request, template_name=template_name)
