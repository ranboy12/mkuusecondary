import datetime as datetime
from _ast import Import

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def student_entry(request):
    get_date = datetime.now().date()
    get_current_year = get_date.year
    students = Student.objects.filter(entry_date__year=get_current_year)
    form = EntryForm(request.POST)

    if request.POST:

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.registerer = request.user
            save_form.save()

            if save_form:
                messages.success(request, f"Student Entered  successfully.")

    else:
        form = EntryForm()

    context = {
        'student': students,
        'form': form,
        'year': get_current_year

    }
    return render(request, 'SRS/student_entry.html', context)


def update_staff_detail(request, object_pk):
    try:
        instance = User.objects.get(id=object_pk)
    except User.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('SRS:staff_entry')
    else:
        form = StaffForm(instance=instance)
    context_dict = {'form': form, 'instance': instance}
    return render(request, 'SRS/update_staff_entry.html', context_dict)


def update_student_detail(request, object_pk):
    try:
        instance = Student.objects.get(id=object_pk)
    except Student.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('SRS:entry')
    else:
        form = EntryForm(instance=instance)
    context_dict = {'form': form, 'instance': instance}
    return render(request, 'SRS/update_student_entry.html', context_dict)


def update_teaching_workload(request, object_pk):
    try:
        instance = WorkLoad.objects.get(id=object_pk)
    except WorkLoad.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = WorkLoadForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('SRS:workload_setting')
    else:
        form = WorkLoadForm(instance=instance)
    context_dict = {'form': form, 'instance': instance}
    return render(request, 'SRS/update_teaching_workload.html', context_dict)


def staff_entry(request):
    get_date = datetime.now().date()
    get_current_year = get_date.year
    TITLE = ('staff', 'teacher', 'ICT Officer', 'System Administrator')
    students = User.objects.filter(title__in=TITLE)
    form = StaffForm(request.POST)

    if request.POST:

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.save()

            if save_form:
                messages.success(request, f"Student Entered  successfully.")

    else:
        form = StaffForm()

    context = {
        'student': students,
        'form': form,
        'year': get_current_year

    }
    return render(request, 'SRS/staff_entry.html', context)
