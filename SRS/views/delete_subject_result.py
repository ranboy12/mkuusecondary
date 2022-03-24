from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from ..models import *
from django.db import transaction, IntegrityError


def delete_subject_result_data(request, subject, rank):
    get_rank = get_object_or_404(Rank, name=rank)
    get_subject = get_object_or_404(Subject, name=subject)

    check_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    with transaction.atomic():
        cards = Result.objects.select_for_update().filter(subject__subject=get_subject,
                                                          registration__rank=get_rank,
                                                          event=check_event).values('registration')

        if cards:
            YearResult.objects.filter(registration__in=cards, event=check_event).delete()
            Result.objects.filter(subject__subject=get_subject, registration__rank=get_rank,
                                  event=check_event).delete()

    return redirect('SRS:subject_results_list', rank=get_rank, subject_name=get_subject)


def register_exam(request, rank, subject):
    get_rank = get_object_or_404(Rank, name=rank)
    get_subject = get_object_or_404(Subject, name=subject)

    check_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    # try:

    cards = Registration.objects.filter(rank=get_rank,
                                        academic_year=check_event.year)

    if cards:
        for i in cards:
            get_combination_subject = CombinationSubject.objects.filter \
                (subject=get_subject, combination=i.combination).first()

            try:

                save_result = Result(
                    registration=i,
                    event=check_event,
                    subject=get_combination_subject,

                )
                save_result.save()
            except IntegrityError:
                continue
    # except:
    #     pass

    return redirect('SRS:subject_results_list', rank=get_rank, subject_name=get_subject)
