#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import json
from datetime import datetime
from ..models import Opcache


# Create your views here.

CONTROLLER = '10.89.151.11'

def _getToken():
	token = ''
	f = open('token-request.json')
	body = json.load(f)
	body = json.dumps(body)
	url = 'http://%s:35357/v3/auth/tokens' % CONTROLLER
	try:
		request = urllib2.Request(url, body)
		request.add_header('Content-type', 'application/json')
		response = urllib2.urlopen(request)
		token = response.headers['X-Subject-Token']
	except Exception, e:
		print e
	return token

def _getdata(req, method, port, path, params):
	data = ''
	code = 500
	url = 'http://' + '%s:%s%s' % (CONTROLLER, port, path)
	try:
		# print "req.session['token']:",req.session['token']
		request = urllib2.Request(url, params)
		request.get_method = lambda: method
		request.add_header('X-Auth-Token', _getToken())
		request.add_header('Content-type', 'application/json')
		response = urllib2.urlopen(request)
		data = response.read()
		code = response.code
	except Exception, e:
		print e
	return data, code


def getTenant(req):
	print 'getTenant'
	if req.method == "GET":
		method = 'GET'
		params = ''
		port = '5000'
		path = '/v2.0/tenants'
		data, code = _getdata(req, method, port, path, params)
		print type(data), data
		# data = {'tokenStatus': 'tokenSuccess', 'tenant': '12345'}
		# print type(json.dumps(data))
		# return HttpResponse(json.dumps(data))
		return HttpResponse(data)

def createvolume(req, body):
	# f = open('create-volume.json')
	# body = json.load(f)

	method = 'POST'
	params = json.dumps(body)
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/volumes' # % tenant_id
	data, code = _getdata(req, method, port, path, params)
	return data, code

def updatevolume(req, volume_id, body):
	# f = open('update-volume.json')
	# body = json.load(f)
	method = 'PUT'
	params = json.dumps(body)
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/volumes/%s' % volume_id
	data, code = _getdata(req, method, port, path, params)
	return data, code

def listvolume(req, user):
	method = 'GET'
	opcache = []
	# opcache = Opcache.objects.filter(user=user).filter(params='').filter(category='listvolume')
	# if opcache is not None and len(opcache) >0:
	# 	return HttpResponse(opcache[0].content)

	params = ''
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/volumes/detail' # % tenant_id
	data, code = _getdata(req, method, port, path, params)
	if code == 200:
		o = Opcache()
		o.user = user
		o.category = 'listvolume'
		o.params = params
		o.content = data
		o.save()

	# data = json.loads(data)
	# volumes = dict()
	# volumes['volumes'] = list()
	# for i in range(len(data['volumes'])):
	# 	volumes['volumes'].append(dict())
	# 	if data['volumes'][i]['attachments']:
	# 		volumes['volumes'][i]['attachments'] = 'Attached to ' \
	# 		                                       + data['volumes'][i]['attachments'][0]['server_id'] \
	# 		                                       + ' on ' + data['volumes'][i]['attachments'][0]['device']
	# 	else:
	# 		volumes['volumes'][i]['attachments'] = []
	# 	volumes['volumes'][i]['availability_zone'] = data['volumes'][i]['availability_zone']
	# 	if data['volumes'][i]['encrypted']:
	# 		volumes['volumes'][i]['encrypted'] = 'Yes'
	# 	else:
	# 		volumes['volumes'][i]['encrypted'] = 'No'
	# 	volumes['volumes'][i]['id'] = data['volumes'][i]['id']
	# 	volumes['volumes'][i]['size'] = data['volumes'][i]['size']
	# 	volumes['volumes'][i]['status'] = data['volumes'][i]['status']
	# 	volumes['volumes'][i]['description'] = data['volumes'][i]['description']
	# 	if data['volumes'][i]['bootable'] == 'true':
	# 		volumes['volumes'][i]['bootable'] = 'Yes'
	# 	else:
	# 		volumes['volumes'][i]['bootable'] = 'No'
	# 	volumes['volumes'][i]['volume_type'] = data['volumes'][i]['volume_type']
	# 	# volumes['volumes'][i]['name'] = data['volumes'][i]['name']
	# 	for key, val in volumes['volumes'][i].items():
	# 		if val == [] or val == None or val == '':
	# 			volumes['volumes'][i][key] = '-'
	# print volumes
	# volumes = dict()
	# volumes['volumes'] = list()
	# for i in range(11):
	# 	volumes['volumes'].append(dict())
	# 	volumes['volumes'][i]['attachments'] = 'test%s' % i
	# 	volumes['volumes'][i]['availability_zone'] = 'test%s' % i
	# 	volumes['volumes'][i]['encrypted'] = 'test%s' % i
	# 	volumes['volumes'][i]['id'] = 'test%s' % i
	# 	volumes['volumes'][i]['size'] = 'test%s' % i
	# 	volumes['volumes'][i]['status'] = 'test%s' % i
	# 	volumes['volumes'][i]['description'] = 'test%s' % i
	# 	volumes['volumes'][i]['bootable'] = 'test%s' % i
	# 	volumes['volumes'][i]['volume_type'] = 'test%s' % i
	# print volumes
	# return HttpResponse(json.dumps(volumes))
	return HttpResponse(data)
	# return data
def deletevolume(req, volumes_id):
	data = ''
	code = 500
	for volume_id in volumes_id:
		method = 'DELETE'
		params = ''
		port = '8776'
		path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/volumes/%s' % volume_id
		data, code = _getdata(req, method, port, path, params)
		if code != 202:
			break
	return data, code

def attachvolume(req, instance_id, body):
	# f = open('attach-volume.json')
	# body = json.load(f)

	method = 'POST'
	params = json.dumps(body)
	port = '8774'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/servers/%s/os-volume_attachments'  % instance_id
	data, code = _getdata(req, method, port, path, params)
	return data, code

def detachvolume(req, instance_id, attachments_id):
	print 'id:', instance_id,attachments_id
	method = 'DELETE'
	params = ''
	port = '8774'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/servers/%s/os-volume_attachments/%s' %(instance_id, attachments_id)
	data, code = _getdata(req, method, port, path, params)
	return data, code

def extendvolume(req, volume_id, body):
	# f = open('extend-volume.json')
	# body = json.load(f)
	method = 'POST'
	params = json.dumps(body)
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/volumes/%s/action' % volume_id
	data, code = _getdata(req, method, port, path, params)
	return data, code

def createsnapshot(req, body):
	# f = open('create-volume.json')
	# body = json.load(f)
	print "body", body
	method = 'POST'
	params = json.dumps(body)
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/snapshots' # % tenant_id
	data, code = _getdata(req, method, port, path, params)
	return data, code

def listsnapshot(req):
	method = 'GET'
	params = ''
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/snapshots/detail' # % tenant_id
	data, code = _getdata(req, method, port, path, params)
	return HttpResponse(data)

def updatesnapshot(req, snapshot_id, body):
	method = 'PUT'
	params = json.dumps(body)
	port = '8776'
	path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/snapshots/%s' % snapshot_id
	data, code = _getdata(req, method, port, path, params)
	return data, code

def deletesnapshot(req, snapshots_id):
	data = ''
	code = 500
	for snapshot_id in snapshots_id:
		method = 'DELETE'
		params = ''
		port = '8776'
		path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/snapshots/%s' % snapshot_id
		data, code = _getdata(req, method, port, path, params)
		if code != 202:
			break
	return data, code

def getconsole(req, instance_id, body):
    # f = open('update-volume.json')
    # body = json.load(f)
    #body = {"os-getVNCConsole": {"type": "novnc"}}
    method = 'POST'
    #print "#######getconsole########",body,instance_id
    params = json.dumps(body)
    port = '8774'
    path = '/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/servers/%s/action' % instance_id
    data, code = _getdata(req, method, port, path, params)
    return data, code
