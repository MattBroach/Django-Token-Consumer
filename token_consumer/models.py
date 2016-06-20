from django.db import models
from django.conf import settings


class Token(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='token',
        on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
    
