import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def combination_subject_list(request):
    get_combination_subject = CombinationSubject.objects.all()
    form = CombinationSubjectForm(request.POST)

    if request.POST:

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.created_by = request.user
            save_form.save()

            if save_form:
                messages.success(request, f"Combination Subject Added  successfully.")

    else:
        form = CombinationSubjectForm()

    context = {
        'combination': get_combination_subject,
        'form': form,

    }
    return render(request, 'SRS/combination_subject.html', context)
