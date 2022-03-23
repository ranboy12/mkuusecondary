from django.db import models
from django.conf import settings


from ..models import *

User = settings.AUTH_USER_MODEL


class PaymentItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    amount = models.IntegerField("Amount to be Paid")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    class Meta:
        verbose_name = "Payment Item"
        verbose_name_plural = "Payment Item"

    def __str__(self):
        return "{0} -{1}".format(self.item, self.amount)
