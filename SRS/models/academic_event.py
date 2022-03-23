from .event import *

User = settings.AUTH_USER_MODEL


class AcademicEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE)
    year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE)
    deadline = models.DateField("Event expire date")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        unique_together = ('event', 'rank','year')

        verbose_name = "Academic Event"
        verbose_name_plural = "Academic Events"

    def save(self, *args, **kwargs):
        # student can request a room once per semester
        if self.__class__.objects.filter(event=self.event,
                                         rank=self.rank).count() >= 1 and self.is_active:
            pass
        elif self.__class__.objects.filter(event=self.event,
                                           rank=self.rank).count() >= 1:
            return None

        return super(AcademicEvent, self).save(*args, **kwargs)


    def __str__(self):
        return "{0}-{1}".format(self.event, self.rank)
