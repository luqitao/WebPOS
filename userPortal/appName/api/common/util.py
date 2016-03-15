from urllib2 import URLError, HTTPError
import logging, json, urllib2
from config import configs
import time
import datetime
__author__ = 'aaron'

KEY_STORE_URL = configs.get('key_store')
TIME_OUT = configs.get('time_out')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Util():

    @staticmethod
    def cal_time(date1,date2):
        date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
        date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
        return date2-date1
    # def read_in_chunks(filePath, chunk_size=1024*1024):
    #     """
    #     Lazy function (generator) to read a file piece by piece.
    #     Default chunk size: 1M
    #     You can set your own chunk size
    #     """
    #     file_object = open(filePath)
    #     while True:
    #         chunk_data = file_object.read(chunk_size)
    #         if not chunk_data:
    #             break
    #         yield chunk_data

    @staticmethod
    def validate_parameter(*args, **dict):
        for key in args:
            if key in dict and len(dict.get(key)) > 0:
                continue
            return False
        return True

    @staticmethod
    def createRequest(url, action,user,content_ype=None):
        code,x_token = Util._get_token(user)
        token=x_token['token']
        req = urllib2.Request(url)
        req.get_method = lambda: action
        header_value = "application/json"
        if content_ype == 'stream':
            header_value = "application/octet-stream"
        elif content_ype == 'patch':
            header_value = "application/openstack-images-v2.1-json-patch"

        req.add_header("Content-Type", header_value)
        req.add_header("X-Auth-Token", token)
        return req

    # @staticmethod
    # def get_user_detail(**user):#1201 Normal response codes: 204 {'tenant_id':tenantId}
    #     method_name = 'get_user_detail'
    #     req = Util.createRequest(KEY_STORE_URL+"v3/users/%s" % user.get('userid'), 'GET',user)
    #     try:
    #         response = urllib2.urlopen(req, timeout=TIME_OUT)
    #         obj = response.read()
    #         if obj and len(obj):
    #             code = response.code
    #             content = json.loads(obj)
    #             logger.debug(method_name+" code:" + str(code))
    #             if code == 200:
    #                 user = content['user']
    #                 domain_id = user['domain_id']
    #                 project_id = user['default_project_id']
    #
    #                 domain_obj=Util.get_domain_detail(domain_id,user)
    #                 if domain_obj[0]==200:
    #                     print 'domain',domain_obj[1]['domain']['name']
    #
    #                 project_obj = Util.get_project_detail(project_id,user)
    #                 if project_obj[0]==200:
    #                     print 'project',project_obj[1]['project']['name']
    #                 return code,{"domain_name":domain_obj[1]['domain']['name'],"project_name":project_obj[1]['project']['name']}
    #             else:
    #                 return code,"error:error"
    #     except HTTPError, e:
    #                 logger.error(method_name+' Error code: '+str(e.code))
    #                 if 404 == e.code:
    #                     logger.error(method_name+' failed.Reason: not found the User')
    #     except URLError, e:
    #                 logger.error(method_name+' URLError: '+str(e.reason))
    #
    #
    # @staticmethod
    # def get_domain_detail(domain_id,user):#1201 Normal response codes: 204 {'tenant_id':tenantId}
    #     method_name = 'get_domain_detail'
    #     req = Util.createRequest(KEY_STORE_URL+"/v3/domains/%s" % domain_id, 'GET',user)
    #     try:
    #         response = urllib2.urlopen(req, timeout=TIME_OUT)
    #         obj = response.read()
    #         if obj and len(obj):
    #             code = response.code
    #             content = json.loads(obj)
    #             logger.debug(method_name+" code:" + str(code))
    #             return code,content
    #     except HTTPError, e:
    #                 logger.error(method_name+' Error code: '+str(e.code))
    #                 if 404 == e.code:
    #                     logger.error(method_name+' failed.Reason: not found the Domain')
    #     except URLError, e:
    #                 logger.error(method_name+' URLError: '+str(e.reason))
    #
    # @staticmethod
    # def get_project_detail(project_id,user):#1046
    #     method_name = 'get_project_detail'
    #     req = Util.createRequest(KEY_STORE_URL+"/v3/projects/%s" % project_id, 'GET', user)
    #     try:
    #         response = urllib2.urlopen(req, timeout=TIME_OUT)
    #         obj = response.read()
    #         code = response.code
    #         if obj and len(obj):
    #             content = json.loads(obj)
    #             logger.debug(method_name+" code:" + str(response.code)+" content:" + str(content))
    #             return code, content
    #         else:
    #             logger.error(method_name+" code:" + str(response.code))
    #             return code,{"error":"error"}
    #     except HTTPError, e:
    #             logger.error(method_name+' Error code: '+str(e.code))
    #     except URLError, e:
    #             logger.error(method_name+' URLError: '+str(e.reason))



    @staticmethod
    def _get_token(user):
        '''
          get token from the server backend
        '''
        token, code = '', ''
        methodName = 'getToken'
        url = KEY_STORE_URL+'v3/auth/tokens'
        f = open('token-request.json')
        body = json.load(f)
        body['auth']['identity']['password']['user']['name'] = user['username']
        body['auth']['identity']['password']['user']['password'] = user['password']
        body = json.dumps(body)
        headers = {"Content-type":"application/json"}
        req = urllib2.Request(url, body, headers)

        try:
            response = urllib2.urlopen(req,body, timeout=TIME_OUT)
            token = response.headers['X-Subject-Token']

            content = response.read()
            code = response.code
            user_id = eval(content)['token']['user']['id']
            roles = eval(content)['token']['roles']
            project_id = eval(content)['token']['project']['id']
            project_name = eval(content)['token']['project']['name']
            project_domain_name = eval(content)['token']['project']['domain']['name']
            user_domain_name = eval(content)['token']['user']['domain']['name']
            return code,{"token":token,"userid":user_id,"userroles":roles,"projectid":project_id,"user_domain_name":user_domain_name,"project_domain_name":project_domain_name,"project_name":project_name}
        except HTTPError, e:
            logging.debug(methodName+' Error code: '+(e.message))
            code = 401
            return code,token
        except URLError, e:
            logging.debug(methodName+' URLError: '+str(e.reason))
            code = e
            return code,token
        except Exception, e:
            if str(e)=='timed out':
                logging.debug(methodName+' URLError: '+str(e))
                code = e
                return code,token
            else:
                logging.debug(methodName+' URLError: ', str(e))
                code = e
                return code,token

