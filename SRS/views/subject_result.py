import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def subject_result(request, rank, subject, combination):
    get_subject = get_object_or_404(Subject, name=subject)

    get_rank = get_object_or_404(Rank, name=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)

    get_combination = get_object_or_404(Combination, name=combination)
    get_subjects_combination = CombinationSubject.objects.get(subject=get_subject, combination=get_combination)

    get_results = Result.objects.filter(subject=get_subjects_combination, registration__rank=get_rank, event=get_event)

    context = {
        'results': get_results,
        'subject': get_subject,
        'rank': get_rank,
        'event': get_event,
        'combination': get_combination,
        'get_subjects_combination': get_subjects_combination,

    }
    return render(request, 'SRS/subject_results.html', context)


def student_character(request, rank, combination):
    get_rank = get_object_or_404(Rank, name=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    get_character = Character.objects.all().order_by('id').distinct()

    get_combination = get_object_or_404(Combination, name=combination)

    get_results = YearResult.objects.filter(
        registration__in=Result.objects.filter(subject__combination=get_combination, registration__rank=get_rank,
                                               event=get_event).values('registration'))
    get_assessment = StudentCharacter.objects.filter(
        registration__in=Result.objects.filter(subject__combination=get_combination, registration__rank=get_rank,
                                               event=get_event).values('registration')).order_by('character__id')
    data = YearResult.objects.filter(
        registration__in=Result.objects.filter(subject__combination=get_combination, registration__rank=get_rank,
                                               event=get_event).values('registration')).exclude(
        registration__in=StudentCharacter.objects.all().values('registration')).count()

    context = {
        'results': get_results,
        'rank': get_rank,
        'event': get_event,
        'combination': get_combination,
        'character': get_character,
        'assessment': get_assessment,
        'data':data

    }
    return render(request, 'SRS/student_character.html', context)
