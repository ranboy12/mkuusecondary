import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def subject_teacher(request):
    get_user = User.objects.get(title="teacher", id=request.user.id)
    get_event = AcademicEvent.objects.filter(is_active=True).first()
    get_workload = WorkLoad.objects.filter(staff=get_user)

    context = {
        'workload': get_workload,
        'event': get_event,

    }
    return render(request, 'SRS/subject_teacher.html', context)


def subject_results_list(request, rank, subject_name):
    get_user = User.objects.get(title="teacher", id=request.user.id)
    get_subject = get_object_or_404(Subject, name=subject_name)

    get_rank = get_object_or_404(Rank, name=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    get_results = Result.objects.filter(subject__subject=get_subject, registration__rank=get_rank, event=get_event)

    context = {
        'result': get_results,
        'subject': get_subject,
        'rank': get_rank,

        'event': get_event,

    }
    return render(request, 'SRS/teacher_subject_results.html', context)
