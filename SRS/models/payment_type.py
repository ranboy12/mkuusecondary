from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Type(models.Model):
    TypeCode={
        ('EC', 'Direct Cost'),
        ('OC', 'Development Cost'),
    }
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    code = models.CharField(max_length=45,choices=TypeCode,default="EC")
    account = models.CharField("Payment account",max_length=45, null=False, blank=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = "Payment Type"
        verbose_name_plural = "Payment Type"

    def __str__(self):
        return self.name
