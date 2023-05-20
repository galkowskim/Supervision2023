from base.models import CustomUser
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class JobAdvertisement(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class ProrityLevels(models.TextChoices):
        LOW = "C", _('Low')
        MEDIUM = "B", _("Medium")
        HIGH = 'A', _("High")

    priority_level = models.CharField(
        max_length=1,
        choices=ProrityLevels.choices,
        default=ProrityLevels.MEDIUM,
    )

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'priority_level'
