
from ..models import *


class WorkLoad(models.Model):

    staff = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=False)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE, null=False)
    year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('staff','subject','rank','year')

        verbose_name = "Academic WorkLoad"
        verbose_name_plural = "Academic WorkLoad"

    def __str__(self):
        return "{0}-{1}".format(self.staff,self.subject)
