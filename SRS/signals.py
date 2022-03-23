from django.db import transaction
from django.db.models import Sum

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import request

from .models import *


@receiver(post_save, sender=YearResult, dispatch_uid='update_total_weight')
def create_investment(sender, instance, created, raw=False, **kwargs):
    if created and not raw:
        with transaction.atomic():
            cards = Result.objects.select_for_update().filter(registration=instance.registration,
                                                              event=instance.event
                                                              ).order_by('-marks')
            if cards:

                total_weight = 0

                for mark in cards:
                    total_weight = total_weight + mark.marks
                    get_year_result = YearResult.objects.filter(id=instance.id).update(weight=total_weight)


@receiver(post_save, sender=Student, dispatch_uid='create_registration_of_new_user')
def create_registration(sender, instance, created, **kwargs):
    if created:
        get_status = Status.objects.get(code="NOT PAID")
        year = AcademicYear.objects.all().order_by('-id').first()
        save_registration = Registration(student=instance, rank=instance.entry_rank, status=get_status,
                                         academic_year=year, is_active=True, )
        save_registration.save()


@receiver(post_save, sender=Payment, dispatch_uid='calculate_the_remaining_cost')
def remaining_cost(sender, instance, **kwargs):
    try:
        get_latest_balance = Payment.objects.filter(
            registration=instance.registration, structure__type=instance.structure.type).order_by(
            '-id')
        get_previous_balance = get_latest_balance[1]

        if get_previous_balance.due > 0:
            get_remaining = get_previous_balance.due - instance.amount
            Payment.objects.filter(id=instance.id).update(due=get_remaining)
            get_status = Status.objects.get(code="PARTIAL PAID")
            save_registration = Registration.objects.get(id=instance.registration.id)
            save_registration.status = get_status
            save_registration.save()
        else:
            complete_registration = Payment.objects.filter(
                registration=instance.registration, due__lte=0.00).order_by(
                '-id').count()
            if complete_registration == 0:
                get_status = Status.objects.get(code="FULL PAID")
                save_registration = Registration.objects.get(id=instance.registration.id)
                save_registration.status = get_status
                save_registration.save()

    except:
        get_remaining = instance.structure.total - instance.amount
        Payment.objects.filter(id=instance.id).update(due=get_remaining)
        get_status = Status.objects.get(code="PARTIAL PAID")
        save_registration = Registration.objects.get(id=instance.registration.id)
        save_registration.status = get_status
        save_registration.save()


@receiver(post_save, sender=PaymentItem, dispatch_uid='calculate_the_total_cost')
def find_total_fee(sender, instance, **kwargs):
    if instance:
        get_total_fee = PaymentItem.objects.filter(type=instance.type, level=instance.level).aggregate(Sum('amount'))[
            'amount__sum']
        total_update = decimal.Decimal(get_total_fee)
        get_structure = PaymentStructure.objects.filter(type=instance.type, level=instance.level).first()

        get_structure.total = total_update
        # get_structure.created_by = request.
        get_structure.save()


@receiver(post_save, sender=Type, dispatch_uid='create_payment_structure')
def create_payment_structure_total(sender, instance, created, **kwargs):
    if created:
        get_ordinary_level = Level.objects.get(name="O-Level")
        get_advanced_level = Level.objects.get(name="A-Level")

        PaymentStructure.objects.create(type=instance, level=get_ordinary_level)
        PaymentStructure.objects.create(type=instance, level=get_advanced_level)

# @receiver(post_save, sender=Payment, dispatch_uid='update_balance')
# def update_remaining_fee_amount(sender, instance, created, **kwargs):
#     if created:
#         get_latest_balance = InvestmentTracking.objects.filter(
#             investment__account__code=instance.investment.account.invite).order_by(
#             '-id').first()
#         get_user = Investment.objects.filter(account__code=instance.investment.account.invite).order_by('-id').first()
#
#         # print(get_latest_balance.balance)
#
#         save_balance = InvestmentTracking(
#             investment=get_user,
#             total_referral=get_latest_balance.total_referral + decimal.Decimal(float(instance.amount)),
#             total_earning=get_latest_balance.total_earning,
#             total_withdraw=get_latest_balance.total_withdraw,
#
#             balance=get_latest_balance.balance + instance.amount
#         )
#         save_balance.save()
