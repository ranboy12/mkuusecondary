import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from xlsxwriter import Workbook

from ..models import *


def download_csv_template(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    template_name = "student_registration_template"

    name = f"{template_name}.xlsx"
    response['Content-Disposition'] = 'attachment; filename=' + name
    # book = Workbook(response, {'in_memory': True})
    # sheet = book.add_worksheet('sheet1')
    #

    # creating workbook
    wb = Workbook(response, {'in_memory': True})

    # adding sheet
    ws = wb.add_worksheet("sheet1")
    ws.set_column('A:A', 28)
    ws.set_column('B:B', 23)
    ws.set_column('C:C', 23)
    ws.set_column('D:D', 18)
    ws.set_column('E:E', 8)
    ws.set_column('F:F', 20)
    ws.set_column('G:G', 20)
    ws.set_column('H:H', 38)

    # Sheet header, first row
    row_num = 0
    # Add a bold format to use to highlight cells.
    bold = wb.add_format({'bold': 1, 'font_color': 'red', 'font_name': 'Cambria'})

    # bold.set_font_name('Times New Roman')
    # font_style = xlwt.XFStyle()
    # headers are bold
    # font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Registration#', 'First Name', 'Middle Name', 'Last Name', 'Sex', 'Parent Phone', 'Class(Number)',
               'Combination']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], bold)

    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()

    # get your data, from database or from a text file...

    wb.close()
    return response


def staff_entry_template(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    template_name = "staff_entry_template"

    name = f"{template_name}.xlsx"
    response['Content-Disposition'] = 'attachment; filename=' + name
    # book = Workbook(response, {'in_memory': True})
    # sheet = book.add_worksheet('sheet1')
    #

    # creating workbook
    wb = Workbook(response, {'in_memory': True})

    # adding sheet
    ws = wb.add_worksheet("sheet1")
    ws.set_column('A:A', 38)
    ws.set_column('B:B', 23)
    ws.set_column('C:C', 23)
    ws.set_column('D:D', 18)
    ws.set_column('E:E', 8)
    ws.set_column('F:F', 20)
    ws.set_column('G:G', 20)

    # Sheet header, first row
    row_num = 0
    # Add a bold format to use to highlight cells.
    bold = wb.add_format({'bold': 1, 'font_color': 'blue', 'font_name': 'Cambria'})

    # bold.set_font_name('Times New Roman')
    # font_style = xlwt.XFStyle()
    # headers are bold
    # font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Email', 'First Name', 'Middle Name', 'Last Name', 'Sex', 'Phone', 'title']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], bold)

    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()

    # get your data, from database or from a text file...

    wb.close()
    return response
