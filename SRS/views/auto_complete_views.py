import csv, io

from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
# one parameter named request
from ..models import *
from django.contrib.auth.models import User


from dal import autocomplete

from ..models import *


class DistrictAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return District.objects.none()

        qs = District.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
