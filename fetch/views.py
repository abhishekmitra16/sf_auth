from django.shortcuts import render

# Create your views here.
import requests
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .models import *
import json

def get_token():
    params = {
        "grant_type": "password",
        "client_id": "3MVG9fe4g9fhX0E5jSHLvn.5q0v1DuKleC3AUWEIfv6PQpg52TB0rrDyzyj.e8PJdqEraCubfdnyOgeTDErsn",
        "client_secret": "624C34779AFFA5BB49852FF53B23881FBAED3F1ED718D873EA27BFA8FFEC8B30",
        "username": "abhishek@96.com",
        "password": "s2pu6VAaph9HM5pQP1RAO24qwgnCD8ZetPUHczE"
    }
    r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)

    access_token = r.json().get("access_token")
    instance_url = r.json().get("instance_url")

    return access_token, instance_url



def get_data(action, parameters = {}, method = 'get', data = {}):
    """
    Fetch data from Salesforce REST API
    """
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    else:

        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))


def acc():
    acc_result = get_data('/services/data/v52.0/query/', {'q': 'SELECT  Name, Phone, NumberOfEmployees from Account'})
    acc_result = acc_result['records']

    for x in acc_result:
        acc_type = x['attributes']['type']
        acc_name = x['Name']
        acc_phone = x['Phone']
        acc_strength = x['NumberOfEmployees']
        data = {
            "acc_name": acc_name,
            "acc_phone": acc_phone,
            "acc_type": acc_type,
            "acc_strength": acc_strength
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()


def user():
    user_result = get_data('/services/data/v52.0/query/', {'q': 'SELECT Name, Username, Email from User'})
    user_result = user_result['records']

    for x in user_result:
        name = x['Name']
        username = x['Username']
        email = x['Email']
        data = {
            "user_name": name,
            "user_username": username,
            "user_email": email
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

def ct():
    contact_result = get_data('/services/data/v52.0/query/',
                              {'q': 'SELECT AccountId, Name, email, Department from Contact'})
    contact_result = contact_result['records']

    for x in contact_result:
        id = x['AccountId']
        name = x['Name']
        email = x['Email']
        dept = x['Department']
        data = {
            "ct_id": id,
            "ct_name": name,
            "ct_email": email,
            "ct_dept": dept
        }
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()


access_token, instance_url = get_token()


class FetchAcc(generics.ListAPIView):

    acc()


    serializer_class = AccountSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class FetchUser(generics.ListAPIView):

    user()
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class FetchCt(generics.ListAPIView):

    ct()
    serializer_class = ContactSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()



