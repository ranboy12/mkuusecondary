from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Rank(models.Model):
    Ranks = (
        ('Form One', 'Form One'),
        ('Form Two', 'Form Two'),
        ('Form Three', 'Form Three'),
        ('Form Four', 'Form Four'),
        ('Form Five', 'Form Five'),
        ('Form Six', 'Form Six'),

    )
    name = models.CharField(choices=Ranks, max_length=20, null=False, blank=False, unique=True)
    number = models.IntegerField(null=False, blank=False, unique=True, editable=False)

    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def save(self, *args, **kwargs):
        if self.name == "Form One":
            self.number = 1
        elif self.name == "Form Two":
            self.number = 2
        elif self.name == "Form Three":
            self.number = 3
        elif self.name == "Form Four":
            self.number = 4
        elif self.name == "Form Five":
            self.number = 5
        elif self.name == "Form Six":
            self.number = 6

        return super(Rank, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'level',)
        verbose_name = "Rank"
        verbose_name_plural = "Ranks"

    def __str__(self):
        return self.name
