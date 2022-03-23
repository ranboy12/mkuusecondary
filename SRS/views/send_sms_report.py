# import requests
# import json
#
# from django.template.defaultfilters import join
#
# from ..models import *
#
#
#
# get_student_results = Result.objects.all()
# get_student = AcademicRegistration.objects.filter(id__in=Result.objects.all().values('registration__id')).distinct()
# get_results2 = YearResult.objects.filter(registration__in=Result.objects.all().values('registration'))
#
# url = "https://messaging-service.co.tz/"
#
# payload = json.dumps({
#     "from": "NEXTSMS",
#     "to": "255755422199",
#     "text": "mama "
# })
# headers = {
#     'Authorization': 'Basic aW0yM246MjNuMjNu',
#     'Content-Type': 'application/json',
#     'Accept': 'application/json'
# }
#
# def send_sms(request):
#     response = requests.request("POST", url, headers=headers, data=payload)
#     print(response.text)
#     return response
#
#



import requests

url = "https://messaging-service.co.tz/"

headers = {'Authorization': 'Basic MDc1NTQyMjE5OTpmcmFua2xpY2lvdXMyMDIz',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'application/json'}

data = {
        'from': 'NEXTSMS',

        'message': "Hello world !",
        'to': '+255755422199'}


def send_sms():
    response = requests.post( url = url, headers = headers, data = data )
    return response


print( send_sms().json() )