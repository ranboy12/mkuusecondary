import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def academic_events(request):
    get_academic_event = AcademicEvent.objects.all()
    form = AcademicEventForm(request.POST)

    if request.POST:

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.created_by = request.user
            save_form.save()

            if save_form:
                messages.success(request, f"Event initiated  successfully.")

    else:
        form = AcademicEventForm()

    context = {
        'event': get_academic_event,
        'form': form,

    }
    return render(request, 'SRS/academic_event.html', context)
