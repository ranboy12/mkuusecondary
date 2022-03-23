from .academic_event import *
from .combination_subject import *
from .student_registration import *

User = settings.AUTH_USER_MODEL


class YearResult(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    event = models.ForeignKey(AcademicEvent, on_delete=models.CASCADE)
    division = models.CharField(max_length=12, editable=False)
    point = models.IntegerField(blank=True, null=True, editable=False)
    weight = models.IntegerField(default=0)
    is_sent = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.weight > 0:
            pass

        elif self.event.rank.level.name == "O-Level":
            if 17 >= self.point >= 7:
                self.division = "1"

            elif 21 >= self.point >= 18:
                self.division = "2"

            elif 25 >= self.point >= 22:
                self.division = "3"

            elif 33 >= self.point >= 26:
                self.division = "4"
            elif 35 >= self.point >= 34:
                self.division = "Zero"

        elif self.event.rank.level.name == "A-Level":
            if 9 >= self.point >= 3:
                self.division = "1"

            elif 12 >= self.point >= 10:
                self.division = "2"

            elif 17 >= self.point >= 13:
                self.division = "3"

            elif 19 >= self.point >= 18:
                self.division = "4"
            elif 21 >= self.point >= 20:
                self.division = "Zero"

        return super(YearResult, self).save(*args, **kwargs)

    class Meta:
        # unique_together = ('registration', 'event')
        verbose_name = "Academic Year Result"
        verbose_name_plural = "Academic Year Results"

    def __str__(self):
        return "{0}-{1}".format(self.registration, self.event)
