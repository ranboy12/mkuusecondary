from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Item(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Item"

    def __str__(self):
        return self.name
