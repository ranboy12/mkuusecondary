from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from ..models import *
from django.db import transaction


def delete_subject_result_data(request, subject, rank):
    get_rank = get_object_or_404(Rank, name=rank)
    get_subject = get_object_or_404(Subject, name=subject)

    check_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    with transaction.atomic():
        cards = Result.objects.select_for_update().filter(subject__subject=get_subject,
                                                          registration__student__rank=get_rank,
                                                          event=check_event).values('registration')

        if cards:
            YearResult.objects.filter(registration__in=cards, event=check_event).delete()
            Result.objects.filter(subject__subject=get_subject, registration__student__rank=get_rank,
                                  event=check_event).delete()

    return redirect('SRS:subject_results_list', rank=get_rank, subject_name=get_subject)
