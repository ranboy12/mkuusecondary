from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from ..models import *

User = settings.AUTH_USER_MODEL


def home(request):
    get_name = request.user.title

    return render(request, 'SRS/user_home.html', {'position': get_name})
