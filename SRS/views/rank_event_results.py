import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def rank_event_results(request):
    get_user = User.objects.get(title="teacher", id=request.user.id)
    get_event = AcademicEvent.objects.filter(is_active=True)
    get_rank = AcademicRegistration.objects.filter(coordinator=get_user).distinct('rank')

    context = {
        'rank': get_rank,
        'event': get_event,


    }
    return render(request, 'SRS/rank_event_results.html', context)
