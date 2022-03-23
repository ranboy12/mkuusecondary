import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from xlsxwriter import Workbook

from ..models import *


def download_subject_result_data(request, subject, rank):
    get_rank = get_object_or_404(Rank, name=rank)
    get_subject = get_object_or_404(Subject, name=subject)
    # get_combination = get_object_or_404(Combination, name=combination)
    # get_combination = get_object_or_404(CombinationSubject, id=combination)
    check_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    template_name = str(rank) + "_" + str(subject) + "_" + "_" + str(check_event.year)

    name = f"{template_name}.xlsx"
    response['Content-Disposition'] = 'attachment; filename=' + name
    # book = Workbook(response, {'in_memory': True})
    # sheet = book.add_worksheet('sheet1')
    #

    # creating workbook
    wb = Workbook(response, {'in_memory': True})

    # adding sheet
    ws = wb.add_worksheet("sheet1")
    ws.set_column('B:B', 18)
    ws.set_column('C:C', 30)
    ws.set_column('D:D', 33)
    ws.set_column('E:E', 11)
    ws.set_column('F:F', 19)

    # Sheet header, first row
    row_num = 0
    # Add a bold format to use to highlight cells.
    bold = wb.add_format({'bold': 1, 'font_color': 'red', 'font_name': 'Cambria'})

    # bold.set_font_name('Times New Roman')
    # font_style = xlwt.XFStyle()
    # headers are bold
    # font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['S/N', 'Registration#', 'Full Name', 'Class', 'Combination', 'Subject', 'Marks']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], bold)

    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()

    # get your data, from database or from a text file...
    data = Result.objects.filter(subject__subject=get_subject, registration__rank=get_rank, event=check_event)
    for my_row in data:
        get_name = f"{my_row.registration.student.first_name} {my_row.registration.student.middle_name} {my_row.registration.student.last_name} "
        get_class = f"{my_row.registration.rank.name}"
        get_subject = f"{my_row.subject.subject.name}"
        get_reg_number = f"{my_row.registration.student.admission}"
        get_combination = f"{my_row.subject.combination.name}"
        row_num = row_num + 1
        ws.write(row_num, 0, row_num)
        ws.write(row_num, 1, get_reg_number)
        ws.write(row_num, 2, get_name)
        ws.write(row_num, 3, get_class)

        ws.write(row_num, 4, get_combination)
        ws.write(row_num, 5, get_subject)
        ws.write(row_num, 6, my_row.marks, bold)

    wb.close()
    return response


def download_assessment_template(request, rank, combination):
    get_rank = get_object_or_404(Rank, name=rank)
    get_combination = get_object_or_404(Combination, name=combination)

    check_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    template_name = str(get_rank.name) + "_" + str(get_combination.name) + "_assessment"

    name = f"{template_name}.xlsx"
    response['Content-Disposition'] = 'attachment; filename=' + name
    # book = Workbook(response, {'in_memory': True})
    # sheet = book.add_worksheet('sheet1')
    #

    # creating workbook
    wb = Workbook(response, {'in_memory': True})

    # adding sheet
    ws = wb.add_worksheet("sheet1")
    ws.set_column('A:A', 5)
    ws.set_column('B:B', 15)
    ws.set_column('C:C', 22)
    ws.set_column('D:D', 10)
    ws.set_column('E:E', 10)


    # Sheet header, first row
    row_num = 0
    # Add a bold format to use to highlight cells.
    bold = wb.add_format({'bold': 1, 'font_color': 'black', 'font_name': 'Cambria'})

    # bold.set_font_name('Times New Roman')
    # font_style = xlwt.XFStyle()
    # headers are bold
    # font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['S/N', 'Registration#', 'Full Name', 'Class', 'Division', '901', '902', '903', '904', '905', '906',
               '907', '908', '909', '910', '911']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], bold)

    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()

    # get your data, from database or from a text file...
    data = YearResult.objects.filter(
        registration__in=Result.objects.filter(subject__combination=get_combination, registration__rank=get_rank,
                                               event=check_event).values('registration')).exclude(registration__in=StudentCharacter.objects.all().values('registration'))

    for my_row in data:
        get_name = f"{my_row.registration.student.first_name} {my_row.registration.student.middle_name} {my_row.registration.student.last_name} "
        get_class = f"{my_row.registration.rank.name}"
        get_result = f"{my_row.division}. {my_row.point}  "
        get_reg_number = f"{my_row.registration.student.admission}"
        row_num = row_num + 1
        ws.write(row_num, 0, row_num)
        ws.write(row_num, 1, get_reg_number)
        ws.write(row_num, 2, get_name)
        ws.write(row_num, 3, get_class)

        ws.write(row_num, 4, get_result, bold)

    wb.close()
    return response
