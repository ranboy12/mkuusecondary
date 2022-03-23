import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def student_academic_year(request):
    get_date = datetime.now().date()
    get_current_year = get_date.year
    get_academic_year = get_object_or_404(AcademicYear, year=get_current_year)
    students = Registration.objects.filter(academic_year=get_academic_year)
    form = RegistrationForm(request.POST)

    if request.POST:

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.year = get_academic_year
            save_form.save()

            if save_form:
                messages.success(request, f"Student Academic Registered  successfully.")

    else:
        form = RegistrationForm()

    context = {
        'registration': students,
        'form': form,
        'year': get_current_year

    }
    return render(request, 'SRS/student_academic_year.html', context)
