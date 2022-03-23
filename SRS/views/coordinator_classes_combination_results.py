import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def coordinator_classes_combination_results(request, rank):
    get_user = User.objects.get(title="teacher", id=request.user.id)
    get_class = get_object_or_404(Rank, name=rank)
    get_event = AcademicEvent.objects.filter(is_active=True, rank=get_class)
    get_combination = Registration.objects.filter(rank=get_class).values('rank__name','combination__name','combination__id').distinct()
    context = {
        'combination': get_combination,
        'event': get_event,
        'rank': get_class,

    }
    return render(request, 'SRS/coordinator_classes_combination_results.html', context)
