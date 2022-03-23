from django.conf import settings

from .. import models
from ..models import *

User = settings.AUTH_USER_MODEL


class Registration(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE)
    combination = models.ForeignKey('Combination', on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    is_registered = models.BooleanField("Registration Status", default=False)
    is_active = models.BooleanField(default=False)
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registration"

    def __str__(self):
        return "{0} -{1}".format(self.student, self.status)
