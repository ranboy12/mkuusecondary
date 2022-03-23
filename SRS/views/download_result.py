from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import os


from ..models import *
from django.http import HttpResponse
from weasyprint import HTML
import tempfile

User = settings.AUTH_USER_MODEL


def download_result(request, rank,combination):
    """Generate pdf."""
    # Model data
    get_rank = get_object_or_404(Rank, name=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)

    get_combination = get_object_or_404(Combination, name=combination)
    get_subjects = Result.objects.filter(subject__combination=get_combination).values('subject__subject__code','subject__subject__is_core','subject__subject__id').order_by(
        'subject__subject__id').distinct()
    get_student = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
            'subject__subject__id').values('registration')).order_by('point','-weight').distinct()

    get_student_results = Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
        'subject__subject__id')
    get_total = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
            'subject__subject__id').values('registration')).values('division').annotate(total=Count('division'))


    # get_total = YearResult.objects.filter(
    #     registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
    #         '-id').values('division')).annotate(total=Count('division'))
    template_name = str(rank)+"_"+str(combination)+"_"+str(get_event.event)+"results"+"_"+str(get_event.year)
    name = f"{template_name}.pdf"
    # Rendered
    html_string = render_to_string('SRS/pdf.html', {'get_student': get_student,'result':get_student_results,'subject':get_subjects,'total':get_total,
                                                    'rank':get_rank,'event':get_event,'combination':get_combination})
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri())
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename='+name
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        # output = open(output.name, 'r')
        output.seek(0)
        response.write(output.read())

    return response


def parent_download_result(request, rank,combination):
    """Generate pdf."""
    # Model data
    get_rank = get_object_or_404(Rank, id=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)

    get_combination = get_object_or_404(Combination, id=combination)
    get_subjects = Result.objects.filter(subject__combination=get_combination).values('subject__subject__code','subject__subject__is_core','subject__subject__id').order_by(
        'subject__subject__id').distinct()
    get_student = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
            'subject__subject__id').values('registration')).order_by('point').distinct()

    get_student_results = Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
        'subject__subject__id')
    get_total = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
            'subject__subject__id').values('registration')).values('division').annotate(total=Count('division'))

    template_name = str(rank)+"_"+str(combination)+"_"+str(get_event.event)+"results"+"_"+str(get_event.year)
    name = f"{template_name}.pdf"

    # get_total = YearResult.objects.filter(
    #     registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
    #         '-id').values('division')).annotate(total=Count('division'))

    # Rendered
    html_string = render_to_string('SRS/pdf.html', {'get_student': get_student,'result':get_student_results,'subject':get_subjects,'total':get_total,
                                                    'rank':get_rank,'event':get_event,'combination':get_combination})
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri())
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename='+name
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        # output = open(output.name, 'r')
        output.seek(0)
        response.write(output.read())

    return response