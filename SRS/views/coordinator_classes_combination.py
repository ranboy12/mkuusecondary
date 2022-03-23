import datetime as datetime
from _ast import Import
from django.db.models import Count
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def coordinator_classes_combination(request, rank):
    get_user = User.objects.get(title="teacher", id=request.user.id)
    get_class = get_object_or_404(Rank, name=rank)
    get_event = AcademicEvent.objects.filter(is_active=True, rank=get_class)
    get_combination = AcademicRegistration.objects.filter(coordinator=get_user, rank=get_class).values('rank__name','combination__name','combination__id').distinct()


    # get_uploading_status=YearResult.objects.filter(registration__combination__name__in=AcademicRegistration.objects.filter(coordinator=get_user, rank=get_class).values('combination__name'), event=get_event).annotate(total=Count('event'))

    context = {
        'combination': get_combination,
        'event': get_event,
        'rank': get_class,
        # 'get_uploading_status': get_uploading_status

    }
    return render(request, 'SRS/coordinator_classes_combination.html', context)
