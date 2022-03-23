from django.db import models
from django.conf import settings

from .student_registration import *

User = settings.AUTH_USER_MODEL


class Status(models.Model):
    STATUS = {
        ('FULL PAID', 'COMPLETE'),
        ('PARTIAL PAID', 'PARTIAL PAID'),
        ('NOT PAID', 'NOT PAID')
    }

    code = models.CharField(choices=STATUS, max_length=30, unique=True, default="NOT PAID")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return "{0}".format(self.code)


class Character(models.Model):
    code = models.CharField(max_length=5, unique=True, null=False)
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Character Assessment Item"
        verbose_name_plural = "Character Assessment Item"

    def __str__(self):
        return "{0}".format(self.code)


class StudentCharacter(models.Model):
    GRADES = {
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    }

    grade = models.CharField(choices=GRADES, max_length=30 )
    remark = models.CharField(max_length=45, null=False, blank=False)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=False)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):

        if self.grade == "A":

            self.remark = "Vizuri sana"

        elif self.grade == "B":

            self.remark = "Vizuri"

        elif self.grade == "C":

            self.remark = "Wastani"
        elif self.grade == "D":

            self.remark = "Dhaifu"
            self.point = 4
        elif self.grade == "F":
            self.remark = "Dhaifu Sana"

        return super(StudentCharacter, self).save(*args, **kwargs)

    class Meta:
        unique_together=('registration','character',)
        verbose_name = "Student Character Assessment"
        verbose_name_plural = "Student Character Assessment"

    def __str__(self):
        return "{0}".format(self.registration)
