from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRank(models.Model):
    name = models.CharField(_('Rank Name'), max_length=50, unique=True)

    def __str__(self):
        return self.name
