from .student_registration import *
from .students_entry import *
from .academic_year import *
from .combination import *

User = settings.AUTH_USER_MODEL


class Coordinator(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE)

    class Meta:
        unique_together=('staff','rank')

        verbose_name = "Class Coordinator"
        verbose_name_plural = "Class Coordinator"

    def __str__(self):
        return "{0}-{1}".format(self.staff, self.rank)
