from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Subject(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    code = models.CharField(max_length=15, null=False, blank=False, unique=True)
    is_core = models.BooleanField("Core Subject", default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name
