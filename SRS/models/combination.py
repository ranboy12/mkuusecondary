from .education_level import *

User = settings.AUTH_USER_MODEL


class Combination(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    subject = models.IntegerField(null=False, blank=False, default=0)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = "Combination"
        verbose_name_plural = "Combinations"

    def __str__(self):
        return self.name
