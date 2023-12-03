from django.db import models

from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    skill = models.CharField(max_length=100, verbose_name=_("Skill Name"))

    def __str__(self) -> str:
        return f"{self.skill}"
