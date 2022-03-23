from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Level(models.Model):
    LEVELS = (
        ('O-Level', 'O-Level'),
        ('A-Level', 'A-Level'),
    )
    name = models.CharField(choices=LEVELS,max_length=45, null=False, blank=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"

    def __str__(self):
        return self.name
