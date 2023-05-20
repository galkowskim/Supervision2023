from django.db import models
from django.utils.translation import gettext_lazy as _


class JobAdvertisement(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    source_page = models.TextField(null=True, blank=True)
    date_of_account_creation = models.DateTimeField(null=True, blank=True)
    fake_probability = models.FloatField(null=True, blank=True)

    class ProrityLevels(models.TextChoices):
        VERY_LOW = "1", _('Very Low')
        LOW = "2", _("Low")
        HIGH_MEDIUM = "3", _("Medium")
        HIGH = '4', _("High")
        VERY_HIGH = '5', _("Very High")

    priority_level = models.CharField(
        max_length=1,
        choices=ProrityLevels.choices,
        default=ProrityLevels.MEDIUM,
    )

    def __str__(self):
        return self.date_added.str() + " " + self.source_page

    class Meta:
        order_with_respect_to = 'priority_level'
