from django.shortcuts import render
from django.http import HttpResponse
from appName.route.key_store_api import _getToken
import json

def doRequest(request):
    context = dict()
    print('doHttpRequest')
    if request.method =="GET" :
        print('getSuccess')
        data = 'getSuccess'
        return HttpResponse(data)
    elif request.method =="POST" :
        print('postSuccess')
        data = 'postSuccess'
        return HttpResponse(data)

def csrftoken(request):
    print('getToken')
    if request.method =="GET" :
        data = {'tokenStatus' : 'tokenSuccess','token':'12345678'}
        #data = {'tokenStatus' : 'tokenSuccess','token':_getToken()}
        return HttpResponse( json.dumps( data ) )