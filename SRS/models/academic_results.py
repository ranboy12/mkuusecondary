from .academic_event import *
from .combination_subject import *
from .student_registration import *

User = settings.AUTH_USER_MODEL


class Result(models.Model):
    marks = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    grade = models.CharField(max_length=1, null=True, blank=True)
    remark = models.CharField(max_length=30, null=True, blank=True)
    point = models.IntegerField(blank=True, null=True)

    event = models.ForeignKey(AcademicEvent, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    subject = models.ForeignKey(CombinationSubject, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.event.rank.level.name == "O-Level":
            if self.marks:
                if 101.0 >= self.marks >= 75.0:
                    self.grade = "A"
                    self.remark = "Excellent"
                    self.point = 1

                elif 74.9 >= self.marks >= 65.0:
                    self.grade = "B"
                    self.remark = "Very Good"
                    self.point = 2
                elif 64.9 >= self.marks >= 45.0:
                    self.grade = "C"
                    self.remark = "Good"
                    self.point = 3
                elif 44.9 >= self.marks >= 30.0:
                    self.grade = "D"
                    self.remark = "Satisfied"
                    self.point = 4
                elif 29.9 >= self.marks >= 0:
                    self.grade = "F"
                    self.remark = "Failed"
                    self.point = 5
            else:

                self.remark = "Incomplete"

        elif self.event.rank.level.name == "A-Level":
            if self.marks:
                if 100.0 > self.marks >= 80.0:
                    self.grade = "A"
                    self.remark = "Excellent"
                    self.point = 1
                elif 79.9 >= self.marks >= 70.0:
                    self.grade = "B"
                    self.remark = "Very Good"
                    self.point = 2
                elif 69.9 >= self.marks >= 60.0:
                    self.grade = "C"
                    self.remark = "Good"
                    self.point = 3
                elif 59.9 >= self.marks >= 50.0:
                    self.grade = "D"
                    self.remark = "Principal"
                    self.point = 4
                elif 49.9 >= self.marks >= 40.0:
                    self.grade = "E"
                    self.remark = "satisfied"
                    self.point = 5
                elif 39.9 >= self.marks >= 35.0:
                    self.grade = "S"
                    self.remark = "Subsidiary"
                    self.point = 6
                elif 34.9 >= self.marks >= 0:
                    self.grade = "F"
                    self.remark = "Fail"
                    self.point = 7
            else:

                self.remark = "Incomplete"

        return super(Result, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('registration', 'event', 'subject')
        verbose_name = "Academic Result"
        verbose_name_plural = "Academic Results"

    def __str__(self):
        return "{0}-{1}".format(self.registration, self.event)
