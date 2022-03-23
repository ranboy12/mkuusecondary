from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
import json

from ..models import *


def index(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if request.user.is_superuser:

                    return redirect("admin:index")
                else:

                    return redirect('SRS:home')

        else:
            # messages.error(request, f"Invalid username or password. please make sure you enter valid credentials")
            messages.success(request, 'Invalid username or password')
            return redirect('SRS:login')

    return render(request, 'SRS/login.html')
