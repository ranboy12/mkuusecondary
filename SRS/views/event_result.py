import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def event_result(request, rank, combination):
    get_rank = get_object_or_404(Rank, name=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)

    get_combination = get_object_or_404(Combination, name=combination)

    get_subjects = Result.objects.filter(subject__combination=get_combination).values('subject__subject__code',
                                                                                      'subject__subject__is_core',
                                                                                      'subject__subject__id').order_by(
        'subject__subject__id').distinct()
    get_student = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
            'subject__subject__code', ).values('registration')).order_by('-weight').distinct()

    get_student_results = Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
        'subject__subject__id')
    sms_to_send = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination,
                                               ).order_by('subject__subject__name').values('registration'),
        is_sent=False).count()

    sms_to_send_f3_f4 = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event
                                               ).order_by(
            'subject__subject__name').values('registration'), is_sent=False).count()
    f3_f4 = range(3, 4)
    f1_f2 = range(1, 2)
    f5_f6 = range(5, 6)

    context = {
        'get_student': get_student,
        'result': get_student_results,
        'subject': get_subjects,
        'combination': get_combination,
        'rank': get_rank,
        'event': get_event,
        'sms': sms_to_send,
        'f3_f4': sms_to_send_f3_f4,
        'range3': f3_f4,
        'range1': f1_f2,
        'range5': f5_f6

    }
    return render(request, 'SRS/event_results.html', context)
