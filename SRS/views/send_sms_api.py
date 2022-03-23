import datetime as datetime
import json
from _ast import Import
import urllib.parse
import requests
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *

from datetime import datetime


def send_event_result_f3_f4(request, rank, combination):
    get_rank = get_object_or_404(Rank, name=rank)

    get_event = AcademicEvent.objects.get(rank=get_rank, is_active=True)


    URL = 'https://apisms.beem.africa/v1/send'
    api_key = '1abab7c78b8a6cb2'
    secret_key = 'MWJiNDBlMTMzYjFlMGFiYWFiZWE0YjRmZDVlZmQ1Zjg5ZmQ0MzgzNzY4YTcyOWFkM2QwNjNhZmZiMDI4MzdlNg=='
    content_type = 'application/json'
    source_addr = 'MKUU SEC'
    apikey_and_apisecret = api_key + ':' + secret_key

    data = []


    #  get_subjects = Result.objects.filter(subject__combination=get_combination).values('subject__subject__code','subject__subject__is_core','subject__subject__id').order_by(
    #     'subject__subject__id').distinct()
    # get_student = YearResult.objects.filter(
    #     registration__in=Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
    #         'subject__subject__id').values('registration')).order_by('point').distinct()

    # get_student_results = Result.objects.filter(event=get_event, subject__combination=get_combination).order_by(
    #     'subject__subject__id')

    get_student = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event).order_by(
            'subject__subject__id').values('registration')).order_by('point','-weight').distinct()
    get_total = YearResult.objects.filter(
        registration__in=Result.objects.filter(event=get_event).order_by(
            'subject__subject__id').values('registration')).distinct().count()
    get_student_results = Result.objects.filter(event=get_event).order_by(
        'subject__subject__id')


    if get_student:
        for index, i in enumerate(get_student, start=1):
            if not i.is_sent:
                test = []
                '''Get name and concatenate them'''
                first_name = i.registration.student.first_name
                last_name = i.registration.student.last_name
                rank = i.registration.rank.code

                student_details = f"Mzazi wa {first_name.upper()} {last_name.upper()} \n{get_event}"

                '''Get phone detail and convert and user id as recipient_id on api'''
                phone = i.registration.student.parent_phone
                phone = phone[1:10]
                phone = '255'+phone

                for x in get_student_results:
                    if i.registration.id == x.registration.id:
                        get_student_rank= x.registration.rank.id
                        get_combination=x.registration.combination.id
                        get_subject = x.subject.subject.code
                        get_marks = x.grade
                        test.append(f"{get_subject}-{get_marks}")

                # subject_results = '\n'.join(map(str, test))
                subject_results = ', '.join(map(str, test))

                get_event_total = f"UFAULU: DIVISION {i.division} {i.point}\nNAFASI : {index}/{get_total}\n kufunga: 10/12/2021\nkufungua: 17/01/2022"

                # get_link = f" https://www.mkuusecondary.ac.tz/class-results-pdf/{rank}/{combination}"
                get_link2 = urllib.parse.quote_plus(rank)


                message_body = f"{student_details}\nMATOKEO\n{subject_results}\n{get_event_total}\nMzazi unakumbushwa kukamilisha Michango ya Shule kwa wakati"
                # print(message_body)

                first_request = requests.post(url=URL, data=json.dumps({
                    'source_addr': source_addr,
                    'schedule_time': '',
                    'encoding': '0',
                    'message': message_body,
                    'recipients': [
                        {
                            'recipient_id': i.id,
                            'dest_addr': phone,
                        },
                    ],
                }),

                                              headers={
                                                  'Content-Type': content_type,
                                                  'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                              },

                                              auth=(api_key, secret_key), verify=False)

                if first_request.status_code == 200:

                    YearResult.objects.filter(id=i.id).update(is_sent=True)


    return redirect('SRS:event_result', rank=rank, combination=combination)
