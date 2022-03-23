import decimal

from django.db import models
from django.conf import settings

from ..models import *

User = settings.AUTH_USER_MODEL


class PaymentStructure(models.Model):
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    minimum = models.DecimalField("minimum amount", max_digits=14, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.total:
            self.minimum = self.total * decimal.Decimal(0.3)

        return super(PaymentStructure, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Payment Structure"
        verbose_name_plural = "Payment Structure"

    def __str__(self):
        return "{0} -{1}".format(self.level, self.total)
