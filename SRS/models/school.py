
from .District import *


class School(models.Model):

    name = models.CharField("Former School", max_length=60, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Schools"
        verbose_name_plural = "School"

    def __str__(self):
        return "{0}".format(self.name)
