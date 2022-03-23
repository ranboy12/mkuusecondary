import random
import string

from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings

from ..models import *

User = settings.AUTH_USER_MODEL


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Student(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    phone_regex = RegexValidator(regex=r'[0][6-9][0-9]{8}', message="Phone number must be entered in the format: "
                                                                    "'0.....'. Up to 10 digits allowed.")
    admission = models.CharField(max_length=100, null=False, blank=False, unique=True)
    entry_number = models.CharField(max_length=100, null=False, blank=False, unique=True)

    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    dob = models.DateField("Date of Birth", blank=True, null=True)  # validators should be a list
    parent_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    residency = models.ForeignKey('District', on_delete=models.CASCADE, null=True, blank=True)
    sex = models.CharField(choices=GENDER, max_length=1, null=True, blank=False)
    entry_rank = models.ForeignKey('Rank', on_delete=models.CASCADE, null=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)
    registerer = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def save(self, *args, **kwargs):
        if len(self.entry_number) < 4:
            self.entry_number = id_generator()

        return super(Student, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Student Entry"
        verbose_name_plural = "Student Entry"

    def __str__(self):
        return self.admission
