from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from ..models import *
from ..forms import *
from ..models import *

User = settings.AUTH_USER_MODEL

from django.contrib.auth.decorators import login_required


@login_required(login_url='/user-authentication/')
def start_registration(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "GET":
            try:
                entry = request.GET.get('phone', False)
                get_account = Registration.objects.filter(student__entry_number=entry).first()

                return redirect('SRS:start_registration', entry=get_account.student.entry_number)
            except:
                pass

        return render(request, 'SRS/registration_home.html')
    else:
        return redirect('SRS:logout')


def register_phase_one(request, entry):
    get_student = get_object_or_404(Student, entry_number=entry)
    direct_acc = Type.objects.get(code="EC")
    development_acc = Type.objects.get(code="OC")
    get_account = Registration.objects.filter(student=get_student).order_by('-id').first()
    get_amount = Payment.objects.filter(registration=get_account).aggregate(total=Sum('amount'))
    get_direct_payment_amount = PaymentStructure.objects.get(level=get_student.entry_rank.level, type__code="EC")
    get_development_payment_amount = PaymentStructure.objects.get(level=get_student.entry_rank.level, type__code="OC")
    get_direct_due= Payment.objects.filter(registration=get_account,structure__type=direct_acc).order_by('-id').first()
    get_development_due= Payment.objects.filter(registration=get_account,structure__type=development_acc).order_by('-id').first()
    context = {
        'get_account': get_account,
        'direct': get_direct_payment_amount,
        'development': get_development_payment_amount,
        'amount': get_amount,
        'direct_due': get_direct_due,
        'development_due': get_development_due,
    }
    return render(request, 'SRS/student_register1.html', context)


def save_student_payments(request):
    if request.method == "POST":
        # try:
        get_id = request.POST['id']
        direct = request.POST['direct']
        development = request.POST['development']
        # get_account = Student.objects.filter(id=id)
        get_account = Student.objects.get(id=get_id)

        get_registration = Registration.objects.filter(student=get_account).order_by('-id').first()

        get_direct_type = Type.objects.get(code="EC")
        get_development_type = Type.objects.get(code="OC")
        get_structure_direct_cost = PaymentStructure.objects.filter(level=get_account.entry_rank.level,
                                                                    type=get_direct_type).first()
        get_structure_development_cost = PaymentStructure.objects.filter(level=get_account.entry_rank.level,
                                                                         type=get_development_type).first()
        save_direct = Payment.objects.create(registration=get_registration, structure=get_structure_direct_cost,
                                             amount=decimal.Decimal(direct), created_by=request.user)
        save_development = Payment.objects.create(registration=get_registration,
                                                  structure=get_structure_development_cost,
                                                  amount=decimal.Decimal(development), created_by=request.user)
        if request.user.title == "Accountant":
            return redirect('SRS:financial_year_debt')
        else:
            return redirect('SRS:complete_registration', student=get_account.admission)


        # except:
        #     return redirect('SRS:registration_home')
    #     messages.error(request, f"Failed, Invalid Entry")


def complete_student_registration(request, student):
    get_student = Student.objects.get(admission=student)
    get_registration = Registration.objects.filter(student=get_student).order_by('-id').first()
    get_payment = Payment.objects.filter(registration=get_registration)

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save(commit=False)

            save_registration = Student.objects.get(admission=student)
            save_registration.parent_phone = form.cleaned_data['parent_phone']
            save_registration.school = form.cleaned_data['school']
            save_registration.dob = form.cleaned_data['dob']
            save_registration.residency = form.cleaned_data['residency']
            save_registration.save()
            if save_registration:
                update_registration = Registration.objects.filter(student=get_student).order_by('-id').first()
                update_registration.is_registered = True
                update_registration.created_by = request.user
                update_registration.save()
                messages.success(request, f"Student is registered Successfully")
                return redirect('SRS:registration_home')

        else:
            pass
    form = RegistrationForm(request.POST)
    context = {
        'form': form,
        'payment': get_payment,
        'student': get_student,
        'get_registration': get_registration,
    }

    return render(request, 'SRS/student_register2.html', context)
