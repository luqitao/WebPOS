# coding=utf-8
import json, urllib2
import logging
from urllib2 import URLError, HTTPError
from common.util import Util
from common.config import configs
from api_exception import APIError

__author__ = 'aaron'

KEY_STORE_URL = configs.get('key_store')
CINDER_URL = configs.get('cinder')
NOVA_URL = configs.get('nova')
TIME_OUT = configs.get('time_out')
#logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def list_project(user):#1046
    method_name = 'list_project'
    req = Util.createRequest(KEY_STORE_URL+"/v3/projects", 'GET',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(response.code)+" content:" + str(content))
        return code, content
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(' URLError: ', e.reason)

# /v2/​{tenant_id}​/os-quota-sets/​{tenant_id}​
def list_project_quota(user, admin_project_id , project_id):#10460d40d7dffdc84e97856358ec02f3917d
    method_name = 'list_project_quota'
    req = Util.createRequest(CINDER_URL+"v2/%s/os-quota-sets/%s" %(admin_project_id,project_id),'GET',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(response.code)+" content:" + str(content))
        return code, content
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(' URLError: ', e.reason)


# /v2/​{tenant_id}​/os-quota-sets/​{tenant_id}​
def update_project_quota(user,admin_project_id,project_id,**quota):#1046
    method_name = 'update_project_quota'
    req = Util.createRequest(NOVA_URL+"v2/%s/os-quota-sets/%s" %(admin_project_id,project_id),'PUT',user)
    ## cinder /network/nova all need to update the Quota separatelly
    try:
        response = urllib2.urlopen(req,json.dumps(quota), timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(response.code)+" content:" + str(content))
        return code, content
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(' URLError: ', e.reason)

def delete_project(user, project_ids):#1046
    method_name = 'delete_project'
    req = Util.createRequest(KEY_STORE_URL+"v3/projects/" + project_ids, 'DELETE', user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        code = response.code
        logger.debug(method_name+" code:" + str(code))
        return code
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(' URLError: ', e.reason)

def create_project(user,**project):  #1045 {'project':project}
    method_name = 'create_project'
    parameter = ['project']
    import pdb
    pdb.set_trace()
    if Util.validate_parameter(*parameter, **project):
        req = Util.createRequest(KEY_STORE_URL+"/v3/projects", 'POST',user)
        try:
            response = urllib2.urlopen(req, json.dumps(project), timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                 content = json.loads(obj)
                 project_id = content['project'].get('id')
                 code = response.code
                 logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                 user_id=content['project'].get('project_user_id')
                 # if code ==201 and user_id is not None:
                 #     role_id="31fd1d2bb7e741218637e230c13df800"#Need to change roleId
                 #     add_user_to_project(user,project_id,user_id,role_id)
                 return code,content
            logger.error(method_name+' Error code: '+response.code)

        except HTTPError, e:
                logger.error(method_name+":"+str(e.message))
                if 409 == e.code:
                    raise APIError('create project failed', 'Project  Duplicated')
                else:
                    raise APIError('HttpError,please contact the admin')
        except URLError, e:
                logger.error(method_name+"URLError:"+e.message)
                raise APIError('URLError',e.reason)
    return 'Input project parameter error, create project failed'



def add_user_to_project(user,project_id,user_id,role_id):  #1045 {'project':project}
    method_name = 'add_user_to_project'
    req = Util.createRequest(KEY_STORE_URL+"/v3/projects/%s/users/%s/roles/%s" %(project_id,user_id,role_id), 'PUT',user)
    try:
            response = urllib2.urlopen(req,  timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                 code = response.code
                 logger.debug(method_name+" code:" + str(code))
                 return code
    except HTTPError, e:
                logger.error(method_name+":"+str(e.message))
                if 409 == e.code:
                    raise APIError('create project failed', 'Project  Duplicated')
                else:
                    raise APIError('HttpError,please contact the admin')
    except URLError, e:
                logger.error(method_name+"URLError:"+e.message)
                raise APIError('URLError',e.reason)


def list_user(user,filter=None):#1046
    method_name = 'list_user'
    url = KEY_STORE_URL+"/v3/users"
    if filter:
        url = KEY_STORE_URL+"/v3/users?"+filter
    req = Util.createRequest(url, 'GET',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
            return code,content
        logger.error(method_name+' Error code: '+response.code)
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError('URLError: ', e.reason)


def create_user(userObject,**user_entity):#{'user',user}
    method_name = 'create_user'
    # if Util.validate_parameter(*parameter, **user):
    print 'user_entityxxxxxx',user_entity
    req = Util.createRequest(KEY_STORE_URL+"/v3/users", 'POST',userObject)
    if user_entity.get('user').get('role') is not None:
         role_id = user_entity.get('user')['role']
         del user_entity.get('user')['role']
    try:
        response = urllib2.urlopen(req, json.dumps(user_entity), timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
            if code == 201:
                user = content.get('user')
                role_assign = {'project_id':user['default_project_id'],'user_id':user["id"], 'role_id':role_id}
                code = assign_role_to_user(userObject,**role_assign)
            return code, content
        else:
            logger.error(method_name+' Error code: '+response.code)
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.message))
                if 409 == e.code:
                    raise APIError('create tenant failed', 'User  Duplicated')
                else:
                    raise APIError('HttpError,please contact the admin')
    except URLError, e:
                logger.error(method_name+' URLError: ', e.reason)
                raise APIError('URLError:'+e.reason)


def list_role(user,filter=None):
    method_name = 'list_role'
    url = KEY_STORE_URL+"/v3/roles"
    if filter is not None:
        url = KEY_STORE_URL+"/v3/roles?"+str(filter)
    req = Util.createRequest(url, 'GET',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj is not None and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
            return code,content
        logger.error(method_name+' Error code: '+response.code)
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError('URLError: ', e.reason)


def assign_role_to_user(user,**kargs):#{'project_id':project_id,'user_id':user_id, 'role_id':role_id}
    method_name = 'assign_role_to_user'
    url = KEY_STORE_URL+"v3/projects/%s/users/%s/roles/%s" % (kargs.get('project_id'), kargs.get('user_id'), kargs.get('role_id'))
    req = Util.createRequest(url, 'PUT',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj is not None:
            code = response.code
            logger.debug(method_name+" code:" + str(code))
            return code

    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            raise APIError('HttpError,please contact the admin')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError('URLError: ', e.reason)



def create_tenant(**teant):  #1199{'teant':teant}
    method_name = 'create_tenant'
    parameter = ('teant')
    if Util.validate_parameter(*parameter, **teant):
        req = Util.createRequest(KEY_STORE_URL+"v2.0/tenants/", 'POST')
        try:
            response = urllib2.urlopen(req, json.dumps(teant.get('teant')), timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return content
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 409 == e.code:
                    raise APIError('create tenant failed', 'Tenant  Duplicated,please update the Tenant to create again')
                else:
                    raise APIError('HttpError,please contact the admin')
        except URLError, e:
                logger.error(method_name+' URLError: ', e.reason)
                raise APIError('URLError:'+e.reason)
    return 'Input Parameter error, can not create the user tenant'



def update_user(**user):#1200 {'tenant_id':tenant_id,'teant':teant}
    method_name = 'update_user'
    parameter = ('user_id', 'user')
    if Util.validate_parameter(*parameter, **user):
        user = user.get('user')
        params = json.dumps(teant)
        req = Util.createRequest(KEY_STORE_URL+"v2.0/users/%s" % user.get('tenant_id'), 'POST')
        try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return content
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.message))
                if 409 == e.code:
                    raise APIError(method_name+'  Duplicated,please update the Tenant to create again')
        except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(method_name+' URLError: ', e.reason)
    return 'Input Parameter error, can not update the tenant'


def update_tenant(**tenant):#1200 {'tenant_id':tenant_id,'teant':teant}
    method_name = 'update_tenant'
    parameter = ('tenant_id', 'teant')
    if Util.validate_parameter(*parameter, **tenant):
        # teant = {
        #             "tenant": {
        #                     "id": tenant.get('tenant_id'),
        #                     "name": "ACMExxx corp",
        #                     "description": "A description ...",
        #                     "enabled": True
        #             }
        #          }
        teant = tenant.get('teant')
        params = json.dumps(teant)
        req = Util.createRequest(KEY_STORE_URL+"v2.0/tenants/%s" % tenant.get('tenant_id'), 'POST')
        try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return content
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.message))
                if 409 == e.code:
                    raise APIError(method_name+'  Duplicated,please update the Tenant to create again')
        except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(method_name+' URLError: ', e.reason)
    return 'Input Parameter error, can not update the tenant'


def delete_tenant(**tenant):#1201 Normal response codes: 204 {'tenant_id':tenantId}
    method_name = 'delete_tenant'
    parameter = ['tenant_id']
    if Util.validate_parameter(*parameter, **tenant):
        req = Util.createRequest(KEY_STORE_URL+"v2.0/tenants/%s" % tenant.get('tenant_id'), 'DELETE')
        try:
            response = urllib2.urlopen(req, json.dumps({}), timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                code = response.code
                logger.debug(method_name+" code:" + str(code))
                return code
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError(method_name+' failed.Reason: not found the Tenant')
        except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)
    return 'Input Parameter error, can not delete the  tenant'


def delete_user(user,user_id):#1201 Normal response codes: 204 {'tenant_id':tenantId}
    method_name = 'delete_user'
    req = Util.createRequest(KEY_STORE_URL+"/v3/users/%s" % user_id, 'DELETE',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        code = response.code
        logger.debug(method_name+" code:" + str(code))
        return code
    except HTTPError, e:
        logger.error(method_name+' Error code: '+str(e.code))
        if 404 == e.code:
            raise APIError(method_name+' failed.Reason: not found the User')
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)


def get_end_point(user):#Lists endpoints for a tenant 1217 {'tenant_id':tenant_id,'endpoint_id':endpoint_id}
    method_name = 'get_end_point'
    req = Util.createRequest(KEY_STORE_URL+"/v3/endpoints", 'GET',user)
    try:
            response = urllib2.urlopen(req, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code,content
            logger.error(method_name+' Error code: '+response.code)
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('Reason: not found the endPoint')
    except URLError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                raise APIError(' URLError: ', e.reason)
    return 'Input Parameter error, can\'t  get endpoint'

def get_policy_by_id(**policy):#{'policy_id':policy_id}
    method_name = 'get_policy_by_id'
    parameter = ('policy_id')
    if Util.validate_parameter(*parameter, **policy):
        req = Util.createRequest(KEY_STORE_URL+'v3/policies/%s'+'/topologies/%d/node/%s' % policy.get('policy_id'), 'GET')
        try:
            response = urllib2.urlopen(req, json.dumps({}), timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError(' failed.Reason: not found the policy')
        except URLError, e:
                logger.error(method_name,' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)
    return 'Input Parameter error, can\'t  get policy'


def list_all_policy(**policy_parameter): #/v3/policies{?type,page,per_page} 1125
    method_name = 'listAllPolicy'
    request_parameter = []
    if policy_parameter is not None and len(policy_parameter) > 0 and isinstance(policy_parameter, dict):
        item = 0
        for (key, value) in policy_parameter.items():
            if item == 0:
                request_parameter.append('?'+key)
            else:
                request_parameter.append('&'+key)
            item += 1
            request_parameter.append('='+str(value))
    if len(request_parameter) > 0:
        logger.debug(method_name+'parameter:' + ''.join(request_parameter))
        req = Util.createRequest(KEY_STORE_URL+'/v3/policies%s' % ''.join(request_parameter), 'GET')
    else:
        req = Util.createRequest(KEY_STORE_URL+'/v3/policies', 'GET')
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
            return code, content
        logger.error(method_name+' Error code: '+response.code)
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            if 404 == e.code:
                raise APIError('Reason: not found the endPoint')
    except URLError, e:
            logger.error(method_name, code, content)
            raise APIError(' URLError: ', str(e.reason))



def get_model_url(user):
    code,serivice_content = get_service_list(user)
    url_list = []
    if  code == 200 and len(serivice_content) > 0:
        code, end_point_content = get_end_point(user)
        if code ==200 and len(end_point_content) > 0:
            serivice_list = serivice_content.get('services')
            end_point_list = end_point_content.get('endpoints')
            set_list = set()
            for service in serivice_list:
                for end_point in end_point_list:
                    if service.get('id') == end_point.get('service_id'):
                        url_dictory = {}
                        if service.get('name') in set_list and service.get('url') in set_list:
                            continue
                        else:
                            set_list.add(service.get('name'))
                            set_list.add(service.get('url'))
                            url = end_point.get('url')
                            id_length = url.find('/v')
                            index = int(id_length)
                            url_dictory['name'] = service.get('name')
                            if id_length>0:
                                url_dictory['url'] = end_point.get('url')[0:index]
                            else:
                                url_dictory['url'] = url
                            url_list.append(url_dictory)
    return url_list

def get_user_detail(user):#1201 Normal response codes: 204 {'tenant_id':tenantId}
    method_name = 'get_user_detail'
    req = Util.createRequest(KEY_STORE_URL+"/v3/users/%s" % user.get('userid'), 'GET',user)
    try:
        response = urllib2.urlopen(req,  timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            code = response.code
            content = json.loads(obj)
            logger.debug(method_name+" code:" + str(code))
            return code,content
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError(method_name+' failed.Reason: not found the User')
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)


def get_service_list(user):#1201 Normal response codes: 204 {'tenant_id':tenantId}
    method_name = 'get_service_list'
    req = Util.createRequest(KEY_STORE_URL+"/v3/services", 'GET', user)
    try:
        response = urllib2.urlopen(req,  timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            code = response.code
            content = json.loads(obj)
            logger.debug(method_name+" code:" + str(code))
            return code,content
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError(method_name+' failed.Reason: not found the Endpoint')
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)



if __name__ == "__main__":
    # create_user(**user)
    teant ={
                "tenant": {
                            "name": "Fiberhome776 Cloud corp",
                            "description": "Demo api description",
                            "enabled": True
                            }
           }

    project =  {'project': {'enabled': True, 'name': 'xyyyxx', 'description': 'yyy'}}

    quota={
        "quota_set": {
            "gigabytes": 10,
            "snapshots": 33,
            "volumes": 20,
        }
    }

    quota={"quota_set": {"metadata_items": 169, "injected_file_content_bytes": 10241, "tenant_id": "c3569861d49445318f7d754b76c79c22", "ram": 51200, "instances": 50, "injected_files": 5, "cores": 30,"floating_ips": 20}}
    # print  update_project_quota(user,**quota)

    userinfo= {u'user': {u'email': u'xxx', u'password': u'xxx', u'role': u'31fd1d2bb7e741218637e230c13df800', u'name': u'xxx', u'default_project_id': u'd04021d5a4144b4c9f579fdc1d1c2a9a'}}
    userObject = {u'username': u'admin','password': 'Abc12345'}
    # print get_end_point(userObject)
    print get_model_url(userObject)
    # create_user(userObject,**userinfo)
    # print delete_user(user,'4065f5cb5d244b94a203e4687ff8d84a')
    # print add_user_to_project(user,'4bbe6b6769824c0da6cdaf6609b05772','2c4dd983d6054dc3bb6889cf0d24bc28','31fd1d2bb7e741218637e230c13df800')
