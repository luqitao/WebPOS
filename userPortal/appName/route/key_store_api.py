#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import json
import os
from datetime import datetime
from ..models import Opcache
# Create your views here.


CONTROLLER = '10.89.151.11'

def _getToken(auth):
	token, code = '', ''
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	f = open('token-request.json')
	body = json.load(f)
	body['auth']['identity']['password']['user']['name'] = auth['username']
	body['auth']['identity']['password']['user']['password'] = auth['password']
	body = json.dumps(body)
	url = 'http://%s:35357/v3/auth/tokens' % CONTROLLER

	try:
		request = urllib2.Request(url, body)
		request.add_header('Content-type', 'application/json')
		response = urllib2.urlopen(request)
		token = response.headers['X-Subject-Token']
		code = response.code
	except Exception, e:
		code = e
	return token, code

def _getdata(method, port, path, params):
	data = ''
	url = 'http://' + '%s:%s%s' % (CONTROLLER, port, path)
	try:
		request = urllib2.Request(url, params)
		request.get_method = lambda: method
		request.add_header('X-Auth-Token', _getToken())
		request.add_header('Content-type', 'application/json')
		response = urllib2.urlopen(request)
		data = response.read()
	except Exception, e:
		print e
	return data

def createTenant(req):
	f = open('create-tenant.json')
	body = json.load(f)

	method = 'POST'
	params = json.dumps(body)
	port = '35357'
	path = '/v2.0/tenants'
	data = _getdata(method, port, path, params)
	return HttpResponse(data)

def listTenant(req):
	method = 'GET'
	params = ''
	port = '35357'
	path = '/v2.0/tenants'
        opcache = []
        params = req;
        opcache = Opcache.objects.filter(user=user).filter(params=params).filter(category='listTenant')
        content = ''
        if opcache is not None and len(opcache) >0:
            data = opcache[0].content
        else:
	    data = _getdata(method, port, path, params)
            o = Opcache()
            o.user = user
            o.category = 'listTenant'
            o.params = params
            o.content = data
            o.save()
	data = json.loads(data)
	# return HttpResponse(data)
	return render(req, 'index.html', data)

def deleteTenant(req):
	method = 'DELETE'
	params = ''
	port = '35357'
	path = '/v2.0/tenants/fcf3d5e58a6244a0b26439037fad9b94' # % tenant_id
	data = _getdata(method, port, path, params)
	return HttpResponse(data)

def getEndpoint(req):
	method = 'GET'
	params = ''
	port = '35357'
	path = '/v3/endpoints'
	data = _getdata(method, port, path, params)
	return HttpResponse(data)

def policy(req):
	method = 'GET'
	params = ''
	port = '35357'
	path = '/v3/policies'
	data = _getdata(method, port, path, params)
	return HttpResponse(data)

def credential(req):
	method = 'GET'
	params = ''
	port = '35357'
	path = '/v3/credentials'
	data = _getdata(method, port, path, params)
	return HttpResponse(data)

def getTenant():
	method = 'GET'
	params = ''
	port = '5000'
	path = '/v2.0/tenants'
	data = _getdata(method, port, path, params)
	# return HttpResponse(data)
	return data
