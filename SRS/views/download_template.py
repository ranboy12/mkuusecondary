import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from xlsxwriter import Workbook

from ..models import *


def download_csv_data(request, rank, subject):
    get_rank = get_object_or_404(Rank, name=rank)
    get_subject = get_object_or_404(Subject, name=subject)
    # get_combination = get_object_or_404(Combination, name=combination)
    # get_combination = get_object_or_404(CombinationSubject, id=combination)
    check_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    template_name = str(rank) + "_" + str(subject) + "_" + str(check_event.year) + "_result"

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
    ws.set_column('D:D', 15)
    ws.set_column('E:E', 30)
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
    data = Registration.objects.filter(rank=get_rank, academic_year =check_event.year).\
        exclude(id__in=Result.objects.filter(subject__subject__name=subject).values('registration__id'))
    for my_row in data:
        get_name = f"{my_row.student.first_name} {my_row.student.middle_name} {my_row.student.last_name} "
        get_class = f"{my_row.rank.name}"
        get_subject = f"{get_subject}"
        get_reg_number = f"{my_row.student.admission}"
        get_combination = f"{my_row.combination.name}"
        row_num = row_num + 1
        ws.write(row_num, 0, row_num)
        ws.write(row_num, 1, get_reg_number)
        ws.write(row_num, 2, get_name)
        ws.write(row_num, 3, get_class)

        ws.write(row_num, 4, get_combination)
        ws.write(row_num, 5, get_subject)
        ws.write(row_num, 6, "", bold)

    wb.close()
    return response
