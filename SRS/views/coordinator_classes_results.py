import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def coordinator_classes_results(request):
    get_user = User.objects.get(title="teacher", id=request.user.id)
    get_coordinator = Coordinator.objects.filter(staff=get_user)
    get_registered= Registration.objects.filter(rank__id__in=Coordinator.objects.filter(staff=get_user).values('rank__id')).values('rank__name','combination__name').annotate(total=Count('combination__name'))



    context = {
        'rank': get_coordinator,
        'registered': get_registered,




    }
    return render(request, 'SRS/coordinator_ranks_result.html', context)
