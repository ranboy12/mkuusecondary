from .combination import *
from .subject import *

User = settings.AUTH_USER_MODEL


class CombinationSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    combination = models.ForeignKey(Combination, on_delete=models.CASCADE)
    # teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        unique_together = ('subject', 'combination',)
        verbose_name = "Combination Subject"
        verbose_name_plural = "Combination Subjects"

    def __str__(self):
        return "{0}-{1}".format(self.combination, self.subject)
