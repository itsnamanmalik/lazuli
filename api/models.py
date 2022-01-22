from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomUser(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('Staff Member')