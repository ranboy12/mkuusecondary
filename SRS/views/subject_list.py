import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def subject_list(request):

    get_subject = Subject.objects.all()
    form = SubjectForm(request.POST)

    if request.POST:

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.created_by = request.user
            save_form.save()

            if save_form:
                messages.success(request, f"Subject registered successfully  successfully.")

    else:
        form = SubjectForm()

    context = {
        'subject': get_subject,
        'form': form,

    }
    return render(request, 'SRS/subject.html', context)
