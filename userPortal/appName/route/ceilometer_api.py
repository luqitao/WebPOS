from urllib2 import URLError, HTTPError
from appName.route import cinder_api as keystone

import urllib
import urllib2
import json
import logging

# from user_portal.common.util import Util

# CONTROLLER = 'http://10.89.151.12'
CONTROLLER = 'http://10.89.151.11'
port = ':8777'
base_path = CONTROLLER + port

# token = Util._get_token()
# auth = {'username':'admin', 'password':'Abc12345'}
token = keystone._getToken()

def build_url(path, q, params=None):
    '''This converts from a list of dicts and a list of params to
       what the rest api needs, so from:
    "[{field=this,op=le,value=34},{field=that,op=eq,value=foo}],
     ['foo=bar','sna=fu']"
    to:
    "?q.field=this&q.op=le&q.value=34&
      q.field=that&q.op=eq&q.value=foo&
      foo=bar&sna=fu"
    '''
    if q:
        query_params = {'q.field': [],
                        'q.value': [],
                        'q.op': [],
                        'q.type': []}

        for query in q:
            for name in ['field', 'op', 'value', 'type']:
                query_params['q.%s' % name].append(query.get(name, ''))

        # Transform the dict to a sequence of two-element tuples in fixed
        # order, then the encoded string will be consistent in Python 2&3.
        new_qparams = sorted(query_params.items(), key=lambda x: x[0])
        path += "?" + urllib.urlencode(new_qparams, doseq=True)

        if params:
            for p in params:
                path += '&%s' % p
    elif params:
        path += '?%s' % params[0]
        for p in params[1:]:
            path += '&%s' % p
    return path


# def get_metaname_stat(meta_name, project_id):
#     path = build_path(meta_name)
#     q=[{"field" : "timestamp" , "op" : "ge" , "value" : "2015-09-29T13:34:17" , "type" : "None"},
#     {'field':'project_id','op':'eq','value':project_id}]
#     full_path= build_url(path,q)
#     datas = _action('get_metaname_stat', full_path, 'GET')
#     datas = json.loads(datas)
#
#     for data in datas:
#         print '%s usage %s for this tenant %s'%(meta_name, data['sum'],project_id)


def _action(name, url, method, context = None):
    req = urllib2.Request(url, context)
    req.get_method = lambda : method
    req.add_header('Content-type', 'application/json')
    req.add_header('X-Auth-Token', token)
    try:
        response = urllib2.urlopen(req)
        res = response.read()
        return res
    except HTTPError, e:
        # logging.error(name + ' Error code:', e.code)
        return e.code
    except URLError, e:
        # logging.error(name + ' Error code :', e.reason)
        return e.message


def list_alarms(q = None):
    name = 'list alarms'
    path = base_path + '/v2/alarms'
    method = 'GET'
    fullpath = build_url(path, q)
    alarms = _action(name, fullpath, method)
    return alarms

def create_alarms(data = None):
    name = 'create alarms'
    path = base_path + '/v2/alarms'
    method = 'POST'
    alarms = _action(name, path, method, data)
    return alarms

def show_alarms(alarm_id):
    name = 'show alarms'
    path = base_path + '/v2/alarms/' + alarm_id
    method = 'GET'
    alarms_detail = _action(name, path, method)
    return alarms_detail

def update_alarms(data):
    pass

def delete_alarms(alarm_id):
    name = 'delete alarms'
    path = base_path + '/v2/alarms/' + alarm_id
    method = 'DELETE'
    result = _action(name, path, method)
    return result

def update_alarms_state(alarm_id, state = None):
    name = 'update alarms state'
    path = base_path + '/v2/alarms/' + alarm_id + '/state'
    method = 'PUT'
    if state is not None:
        path += '?state=' + state
    result = _action(name, path, method)
    return result

def show_alarm_state(alarm_id):
    name = 'show alarm state'
    path = base_path + '/v2/alarms/' + alarm_id + '/state'
    method = 'GET'
    state_detail = _action(name, path, method)
    return state_detail

def show_alarm_history(alarm_id):
    name = 'show alarm history'
    path = base_path + '/v2/alarms/' + alarm_id + '/history'
    method = 'GET'
    history = _action(name, path, method)
    return history

def list_meter(q = None):
    name = 'list meter'
    path = base_path + '/v2/meters'
    method = 'GET'
    fullpath = build_url(path, q)
    meter = _action(name, fullpath, method)
    return meter

def show_meter(meter_name, q = None, limit = None):
    name = 'show meter'
    path = base_path + '/v2/meters/' + meter_name
    method = 'GET'
    fullpath = build_url(path, q)
    if limit is not None:
        if q:
            fullpath += '&limit=' + str(limit)
        else:
            fullpath += '?limit=' + str(limit)
    meter_detail = _action(name, fullpath, method)
    return meter_detail

def create_meter():
    pass

def show_meter_statistics(meter_name, q = None, groupby = None, period = None):
    name = 'show meter statistics'
    path = base_path + '/v2/meters/' + meter_name + '/statistics'
    method = 'GET'
    fullpath = build_url(path, q)
    if q:
        if groupby:
            for i in groupby:
                fullpath += '&groupby=' + i
        if period:
            fullpath += '&period=' + str(period)
    else:
        if groupby:
            fullpath += '?groupby=' + groupby
            if period:
                fullpath += '&period=' + str(period)
        else:
            if period:
                fullpath += '?period=' + str(period)
    meter_statistics = _action(name, fullpath, method)
    return meter_statistics

def list_samples(q = None):
    name = 'list samples'
    path = base_path + '/v2/samples'
    method = 'GET'
    fullpath = build_url(path, q)
    samples = _action(name, fullpath, method)
    return samples

def show_samples(sample_id):
    name = 'show samples'
    path = base_path + '/v2/samples/' + sample_id
    method = 'GET'
    sample = _action(name, path, method)
    return sample

def list_resources(q = None):
    name = 'list resources'
    path = base_path + '/v2/resources'
    method = 'GET'
    fullpath = build_url(path, q)
    resources = _action(name, fullpath, method)
    return resources

def show_resource_information(resource_id):
    name = 'show resource information'
    path = base_path + '/v2/resources/' + resource_id
    method = 'GET'
    information = _action(name, path, method)
    return information

def list_capabilities():
    name = 'list capabilities'
    path = base_path + '/v2/capabilities/'
    method = 'GET'
    capabilities = _action(name, path, method)
    return capabilities


if __name__ == "__main__":
    print show_meter_statistics('disk.root.size')

