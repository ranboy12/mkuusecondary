import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def combination_subjects(request, rank, combination):
    get_rank = get_object_or_404(Rank, name=rank)
    get_event = AcademicEvent.objects.filter(is_active=True, rank=get_rank)
    combination =get_object_or_404(Combination, name=combination)

    get_combination = CombinationSubject.objects.filter(combination__name=combination)

    context = {
        'subject': get_combination,
        'rank': get_rank,
        'ranks': get_rank,
        'event': get_event,
        'combination': combination,

    }
    return render(request, 'SRS/academic_event_assessment.html', context)
