import datetime

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from ..models import *
from ..forms import *

User = settings.AUTH_USER_MODEL

from django.contrib.auth.decorators import login_required


@login_required(login_url='/user-authentication/')
def payment_structure_list(request):
    if request.user.is_staff or request.user.is_superuser:
        direct_acc = Type.objects.get(code="EC")
        development_acc = Type.objects.get(code="OC")
        o_level = Level.objects.get(name="O-Level")
        a_level = Level.objects.get(name="A-Level")
        get_o_level_payment_item = PaymentItem.objects.filter(level=o_level)
        get_a_level_payment_item = PaymentItem.objects.filter(level=a_level)
        get_o_level_payment_structure = PaymentStructure.objects.filter(level=o_level)
        get_a_level_payment_structure = PaymentStructure.objects.filter(level=a_level)
        context = {
            'direct_acc': direct_acc,
            'development_acc': development_acc,
            'o_level_item': get_o_level_payment_item,
            'a_level_item': get_a_level_payment_item,
            'o_level_structure': get_o_level_payment_structure,
            'a_level_structure': get_a_level_payment_structure,

        }

        return render(request, 'SRS/payment_structure.html', context)
    else:
        return redirect('SRS:logout')


def payment_items_list(request):
    if request.user.is_staff or request.user.is_superuser:
        direct_acc = Type.objects.get(code="EC")
        development_acc = Type.objects.get(code="OC")
        o_level = Level.objects.get(name="O-Level")
        a_level = Level.objects.get(name="A-Level")
        get_o_level_payment_item = PaymentItem.objects.filter(level=o_level).order_by('type')
        get_a_level_payment_item = PaymentItem.objects.filter(level=a_level).order_by('type')

        context = {
            'direct_acc': direct_acc,
            'development_acc': development_acc,
            'o_level_item': get_o_level_payment_item,
            'a_level_item': get_a_level_payment_item,

        }

        return render(request, 'SRS/school_payments_item.html', context)
    else:
        return redirect('SRS:logout')


def financial_year_debt(request):
    today = datetime.datetime.now()
    o_level = Level.objects.get(name="O-Level")
    a_level = Level.objects.get(name="A-Level")
    status = Status.objects.get(code="PARTIAL PAID")

    get_payment = Payment.objects.filter(registration__status=status).values(
        'registration').annotate(total=Sum('amount'))
    get_student = Registration.objects.filter(id__in=Payment.objects.filter(registration__status=status).values(
        'registration'))

    get_total_required_ordinary_level = PaymentStructure.objects.filter(level=o_level).aggregate(total=Sum('total'))
    get_total_required_advance_level = PaymentStructure.objects.filter(level=a_level).aggregate(total=Sum('total'))

    context = {
        'payment': get_payment,
        'registration': get_student,
        'total_ordinary': get_total_required_ordinary_level,
        'total_advance': get_total_required_advance_level,
        'o_level': o_level,
        'a_level': a_level,

    }
    return render(request, 'SRS/financial_year_debt.html', context)


@login_required(login_url='/user-authentication/')
def financial_year_income(request):
    if request.user.is_staff or request.user.is_superuser:
        today = datetime.datetime.now()
        direct_acc = Type.objects.get(code="EC")
        development_acc = Type.objects.get(code="OC")
        o_level = Level.objects.get(name="O-Level")
        a_level = Level.objects.get(name="A-Level")
        get_o_level_payment = Payment.objects.filter(structure__level=o_level,
                                                     registration__academic_year__year=today.year).values(
            'registration__rank__name').annotate(total=Sum('amount'))
        get_a_level_payment = Payment.objects.filter(structure__level=a_level,
                                                     registration__academic_year__year=today.year).values(
            'registration__rank').annotate(total=Sum('amount'))
        get_income = Payment.objects.filter(registration__academic_year__year=today.year).values(
            'registration__rank').aggregate(total=Sum('amount'))

        context = {
            'direct_acc': direct_acc,
            'development_acc': development_acc,
            'o_level': get_o_level_payment,
            'a_level': get_a_level_payment,
            'income': get_income,

        }

        return render(request, 'SRS/financial_year_income.html', context)
    else:
        return redirect('SRS:logout')

# def register_phase_one(request, entry):
#     get_student = get_object_or_404(Student, entry_number=entry)
#     get_account = Registration.objects.filter(student=get_student).order_by('-id').first()
#     get_amount = Payment.objects.filter(registration=get_account).aggregate(total=Sum('amount'))
#     get_direct_payment_amount = PaymentStructure.objects.get(level=get_student.entry_rank.level, type__code="EC")
#     get_development_payment_amount = PaymentStructure.objects.get(level=get_student.entry_rank.level, type__code="OC")
#     context = {
#         'get_account': get_account,
#         'direct': get_direct_payment_amount,
#         'development': get_development_payment_amount,
#         'amount': get_amount,
#     }
#     return render(request, 'SRS/student_register1.html', context)
#
#
# def save_student_payments(request):
#     if request.method == "POST":
#         # try:
#         get_id = request.POST['id']
#         direct = request.POST['direct']
#         development = request.POST['development']
#         # get_account = Student.objects.filter(id=id)
#         get_account = Student.objects.get(id=get_id)
#
#         get_registration = Registration.objects.filter(student=get_account).order_by('-id').first()
#
#         get_direct_type = Type.objects.get(code="EC")
#         get_development_type = Type.objects.get(code="OC")
#         get_structure_direct_cost = PaymentStructure.objects.filter(level=get_account.entry_rank.level,
#                                                                     type=get_direct_type).first()
#         get_structure_development_cost = PaymentStructure.objects.filter(level=get_account.entry_rank.level,
#                                                                          type=get_development_type).first()
#         save_direct = Payment.objects.create(registration=get_registration, structure=get_structure_direct_cost,
#                                              amount=decimal.Decimal(direct), created_by=request.user)
#         save_development = Payment.objects.create(registration=get_registration,
#                                                   structure=get_structure_development_cost,
#                                                   amount=decimal.Decimal(development), created_by=request.user)
#
#         return redirect('SRS:complete_registration', student=get_account.admission)
#
#         # except:
#         #     return redirect('SRS:registration_home')
#     #     messages.error(request, f"Failed, Invalid Entry")
#
#
# def complete_student_registration(request, student):
#     get_student = Student.objects.get(admission=student)
#     get_registration = Registration.objects.filter(student=get_student).order_by('-id').first()
#     get_payment = Payment.objects.filter(registration=get_registration)
#
#     if request.method == "POST":
#
#         form = RegistrationForm(request.POST)
#
#         if form.is_valid():
#             form.save(commit=False)
#
#             save_registration = Student.objects.get(admission=student)
#             save_registration.parent_phone = form.cleaned_data['parent_phone']
#             save_registration.school = form.cleaned_data['school']
#             save_registration.dob = form.cleaned_data['dob']
#             save_registration.residency = form.cleaned_data['residency']
#             save_registration.save()
#             if save_registration:
#                 update_registration = Registration.objects.filter(student=get_student).order_by('-id').first()
#                 update_registration.is_registered = True
#                 update_registration.created_by = request.user
#                 update_registration.save()
#                 messages.success(request, f"Student is registered Successfully")
#                 return redirect('SRS:registration_home')
#
#         else:
#             pass
#     form = RegistrationForm(request.POST)
#     context = {
#         'form': form,
#         'payment': get_payment,
#         'student': get_student,
#         'get_registration': get_registration,
#     }
#
#     return render(request, 'SRS/student_register2.html', context)
