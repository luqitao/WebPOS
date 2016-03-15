# coding=utf-8
from urllib2 import URLError, HTTPError
import urllib2
import json
import logging
from api_exception import APIError
from common.config import configs
from common.util import Util
# from appName.route.neutron_api import list_ports_by_nobind
# from appName.route.neutron_api import list_network
# from appName.route import neutron_api
from ..models import Opcache

import Queue
import threading


__author__ = 'aaron'

CACHE_SERVER_PARAMS = "/v2/servers"
CACHE_SERVER_CATEGORY = "list_all_server"

#NOVAL request url
NOVAL_URL = configs.get('nova')
TIME_OUT = configs.get('time_out')
#logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
flavor_list = []
#4 days xxm xx s xx second transfer to  the xx year xx day xx hours xx minutes xx seconds
def format_date(str_datetime):
    index_days = 0
    if 'days' in str_datetime:
        index_days = str_datetime.index('days')
    index = 0

    day=0
    if index_days > 0:
        day = str_datetime[0:index_days]
        index = index_days+6

    days = 0
    years = 0
    if int(day) > 365:
        years = int(day)/365
        days = int(day)%365

    string =""
    if years > 0 :
        string +=(str(years)+' year ')
    if days > 0 :
        string +=(str(days)+' day ')
    elif day > 0:
        string +=(str(day)+' day ')

    h = str_datetime[index:index+2]
    m = str_datetime[index+3:index+5]
    s = str_datetime[index+6:index+8]

    if len(h) > 0 and int(h) > 0:
        string += (h+' hours ')
    if len(m) > 0 and int(m) > 0:
        string += (m+' minutes ')
    if len(s) > 0 and int(s) > 0:
        string += (s+' seconds ')

    return string


q = Queue.Queue()

class myThread(threading.Thread):
    def __init__(self,user,server_list,thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        # self.name = name
        self.server_list = server_list
        self.user = user

    def run(self):
        launch_server(self.user, self.server_list,self.thread_id)



def _start_thread(user,server_list):
    threads = []
    thread_id = 1
    # 创建新线程
    for server in server_list:
        thread = myThread(user,server,thread_id)
        thread.start()
        threads.append(thread)
        thread_id += 1
    return threads


def launch_server_by_thread(user,server_list):
    threads = _start_thread(user,server_list)

    for t in threads:
        t.join()
    result = list()
    while not q.empty():
        result.append(q.get())

    print 'xxxxxxx',result
    if len(server_list) == len(result):
        return 202,"Success"
    else:
        return 203,"Create failed "+bytes(len(result)-len(server_list)) +" num"





def networkport_field_data(user):
    """Returns a list of tuples of all networks.

    Generates a list of networks available to the user (request). And returns
    a list of (id, name) tuples.

    :param request: django http request object
    :param include_empty_option: flag to include a empty tuple in the front of
    the list
    :return: list of (id, name) tuples
    """
    from appName.route import neutron_api as neutron_api
    networks = []
    ports = []
    try:
         networks,code = neutron_api.list_network(user,user.get('projectid'), False)
         print 'networks:----',networks
         if code == 200:
             networks_list = networks.get('networks')
             if len(networks_list) >0:
                 networks = [(n.get('id'),n.get('name')) for n in networks_list]
                 # print 'networksxxxx',networks
                 # networks.sort(key=lambda obj: obj[0])
    except Exception as e:
         print e
    if not networks:
            print "No networks available"

    networks=[
        (u'01db79e0-628f-4fb0-a483-c84f923b0728',    u'zportal123111'),
        (u'147fbad0-485d-4ada-ba5d-cf7a25de67bf',    u'huang'),
        (u'23969855-53d3-4300-b3a4-1aeb8981c182',    u'tcxtcxtcx'),
        (u'2f0674bc-663f-45e3-bb98-ac3ea91f65b1',    u'zsh-1'),
        (u'38c7b08b-73da-4561-aab6-f96c6be892ae',    u'tempest_public'),
        (u'3fd6e9ee-6618-46e6-9471-ff12a605e04f',    u'test11'),
        (u'4e4192af-ba9c-4908-8d88-b4b79a22277c',    u'test-vpn-network'),
        (u'52ea0274-692b-4ef2-a37b-d56fc2561af4',    u'cbnet'),
        (u'5c9aadc3-ed0e-42a5-8ba5-71b5c957199c',    u'ext-net'),
        (u'753dd77b-7b77-42f1-9cfc-1d0273bfd670',    u'wangwang'),
        (u'7d1a1cee-dd60-4546-971e-3db05fcdf371',    u'suibiansuibian'),
        (u'90ee0dc5-38f9-4c5f-b206-8ea04966b7de',    u'test-vpn-network-2'),
        (u'9809e635-1ace-4fa9-bbbc-f450df24ba59',    u'net'),
        (u'b91179d1-33d9-414a-8956-34124dd09caa',    u'nnzhang-network'),
        (u'bdbb7cfd-5603-4a0e-9216-34b3ea7e1e8d',    u'wangxuguang'),
        (u'c6ddf9ea-6ccc-4e29-8829-a5c8161515cb',    u'nnzhang-network1'),
        (u'ca6fa325-ed70-455d-a196-8cc02574f982',    u'sisyphuswxg')
    ]

    # networks= [
    #     (u'52ea0274-692b-4ef2-a37b-d56fc2561af4',    u'cbnet'),
    #     (u'5c9aadc3-ed0e-42a5-8ba5-71b5c957199c',    u'ext-net'),
    #     (u'2fca71c5-d15c-4715-b9ac-ff1c707fb35e',    u'gzy-net'),  #meiyou
    #     (u'147fbad0-485d-4ada-ba5d-cf7a25de67bf',    u'huang'),
    #     (u'1d03b190-6854-4992-8096-75c6f55482b0',    u'kly-net-nodhcp'),  #meiyou
    #     (u'9809e635-1ace-4fa9-bbbc-f450df24ba59',    u'net'),
    #     (u'b91179d1-33d9-414a-8956-34124dd09caa',    u'nnzhang-network'),
    #     (u'c6ddf9ea-6ccc-4e29-8829-a5c8161515cb',    u'nnzhang-network1'),
    #     (u'ca6fa325-ed70-455d-a196-8cc02574f982',    u'sisyphuswxg'),
    #     (u'7d1a1cee-dd60-4546-971e-3db05fcdf371',    u'suibiansuibian'),
    #     (u'23969855-53d3-4300-b3a4-1aeb8981c182',    u'tcxtcxtcx'),
    #     (u'38c7b08b-73da-4561-aab6-f96c6be892ae',    u'tempest_public'),
    #     (u'167d6c61-ebcb-411e-9694-1ee84b3e69e7',    u'test-lc'),     #meiyou
    #     (u'4e4192af-ba9c-4908-8d88-b4b79a22277c',    u'test-vpn-network'),
    #     (u'90ee0dc5-38f9-4c5f-b206-8ea04966b7de',    u'test-vpn-network-2'),
    #     (u'3fd6e9ee-6618-46e6-9471-ff12a605e04f',    u'test11'),
    #     (u'4de556c2-1978-479e-a80b-dfe37226a891',    u'vpn2'),     #meiyou
    #     (u'753dd77b-7b77-42f1-9cfc-1d0273bfd670',    u'wangwang'),
    #     (u'bdbb7cfd-5603-4a0e-9216-34b3ea7e1e8d',    u'wangxuguang'),
    #     (u'5e2585a3-018f-41ee-93c2-cac9d15d72e0',    u'yannhua_network2'), #meiyou
    #     (u'01db79e0-628f-4fb0-a483-c84f923b0728',    u'zportal123111'),
    #     (u'2f0674bc-663f-45e3-bb98-ac3ea91f65b1',    u'zsh-1')
    # ]s
    for n in networks:
         #temply ignore ext-net
         if n[1] == 'ext-net':
             continue
         tmpports = neutron_api.list_ports_by_nobind(network_id=n[0])
         tmpports = [(p.get('id'),p.get('ip_address')) for p in tmpports] #fetch the show of the multichose part
         if tmpports:
             ports.extend(tmpports)
         tmpports = []

    ports= [(u'82f35082-5e37-4332-9902-0cd53415c26a', u'192.168.0.221'), (u'8b4d199c-b066-40f8-92f7-d417c031b281', u'192.168.0.220'), (u'6a89143c-27a6-420b-993c-3d419f9b429c', u'10.0.200.200')]
    return ports



def update_server(user, server_id, **kwargs):#513 {'tenant_id':tenant_id,'server_id':server_id,'migrage_value':migrage_value}
    method_name = 'update_server'
    params = json.dumps(kwargs)
    req = Util.createRequest(NOVAL_URL+'v2/%s/servers/%s/action' % (user['projectid'], server_id), 'PUT',user) #500 error 48d8cd602577412c978f0184544e9e1c
    try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('Not found the server')
                else:
                    raise APIError('Reason: '+str(e.message))
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)


def launch_server(user, kwargs, thread_id=None): #{'server':server,'tenant_id':tenant_id}
    method_name = 'launch_server'

    req = Util.createRequest(NOVAL_URL+'v2/%s/servers' % user.get('projectid'), 'POST',user)
    try:
            new_instance = json.dumps(kwargs)
            print 'new_instance',new_instance
            response = urllib2.urlopen(req, new_instance, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                instance_id = content.get('server')['id']
                if thread_id is not None:

                    q.put(thread_id, code)
                if code == 202:
                    try:
                        delete_cache(None, user)
                    except Exception, e:
                        print e
                else:
                    delete_cache(instance_id, user)
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('Reason: not found the server')
    except URLError, e:
                logger.debug(method_name+' URLError: '+str(e.reason))
                raise APIError('URLError: ', e.reason)



def list_all_server(user):#123  #/v2.1/servers/detail    ErrorCode 500
    method_name = 'list_all_server'
    opcache = []
    opcache = Opcache.objects.filter(user=user.get('username')).filter(category=method_name)

    if opcache is not None and len(opcache) > 0:
        content = json.loads(opcache[0].content)
    	return 200, content 
    req = Util.createRequest(NOVAL_URL+'v2/%s/servers/detail' % user['projectid'], 'GET',user) #500 error 48d8cd602577412c978f0184544e9e1c
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            o = Opcache()
            o.user = user.get('username')
            o.category = method_name
            o.content = obj
            o.params = "/v2/servers"
            o.save()
            code = response.code
            # logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
            return code, content
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            if 404 == e.code:
                raise APIError(method_name+' failed.Reason: not found the server')
            # else:
            #     raise APIError('Reason: '+str(e.message))
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(' URLError: ', e.reason)


def list_flavor(user):#621  /v2/{tenant_id}/flavors    ErrorCode 500
    opcache = []

    opcache = Opcache.objects.filter(user=user.get('username')).filter(category='list_flavor')
    if opcache is not None and len(opcache) > 0:
        flavor_list1 = json.loads(opcache[0].content)
        return flavor_list1

    method_name = 'list_flavor'
    req = Util.createRequest(NOVAL_URL+'v2/%s/flavors' % user['projectid'], 'GET', user)
    try:
                response = urllib2.urlopen(req, timeout=TIME_OUT)
                obj = response.read()
                if obj and len(obj):
                    content = json.loads(obj)
                    code = response.code
                    flavor_list_temp = []
                    # logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                    flavor_list_temp.append(code)
                    flavor_list_temp.append(content)
                    if code == 200:
                        for flavor in flavor_list_temp[1]['flavors']:
                            map = {}
                            map['id'] = flavor['id']
                            map['name'] = flavor['name']
                            flavor_list.append(map)

                        o = Opcache()
                        o.user = user
                        o.category = 'list_flavor'
                        o.params = 'v2/flavors'
                        o.content = json.dumps(flavor_list)
                        o.save()

                        return flavor_list
                    else:
                        return ["code",code]
    except HTTPError, e:
                    logger.error(method_name+' Error code: '+str(e.code))
                    if 404 == e.code:
                        raise APIError(method_name+' failed.Reason: not found the flavors')
                    else:
                        raise APIError('Reason: '+str(e.message))
    except URLError, e:
                    logger.error(method_name+' URLError: '+str(e.reason))
                    raise APIError(' URLError: ', e.reason)

    return flavor_list


def migrate_server(user,**kwargs):#513 {'tenant_id':tenant_id,'server_id':server_id,'migrage_value':migrage_value}
    method_name = 'migrate_server'
    params = json.dumps(kwargs.get('migrage_value'))
    req = Util.createRequest(NOVAL_URL+'v2/%s/servers/%s/action' % (user['projectid'], kwargs.get('server_id')), 'POST',user) #500 error 48d8cd602577412c978f0184544e9e1c
    try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('Not found the server')
                else:
                    raise APIError('Reason: '+str(e.message))
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)



def operate_instance(user,**kwargs):#{tenant_id:'tenant_id','server_id':server_id,'reboot_type':reboot_type}
    method_name = 'operate_instance'
    req = Util.createRequest(NOVAL_URL+'v2/%s/servers/%s/action' % (user['projectid'], kwargs.get('server_id')), 'POST',user) #500 error 48d8cd602577412c978f0184544e9e1c
    params = json.dumps(kwargs.get('operate_type'))
    try:
        response = urllib2.urlopen(req, params, timeout=TIME_OUT)
        code = response.code
        logger.debug(method_name+" code:" + str(code))
        # if code ==202:
        #     log =  Loginfo()
        #     log.userid=user["userid"]
        #     log.operate=kwargs.get('operate_type')
        #     log.content = kwargs.get('operate_type')+" instance "
        #     log.save()
        return code
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            if 404 == e.code:
                raise APIError('Reason: not found the server')
            else:
                raise APIError('Reason: '+str(e.message))
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(' URLError: ', e.reason)



def start_stop_server(user,**kwargs):#137 /v2.1/servers/{server_id}/action ErrorCode 500
    #{'tenant_id':tenant_id,'server_id':server_id,'action':action}
    method_name = 'start_stop_server'
    parameter = ('server_id', 'action')
    if Util.validate_parameter(*parameter, **kwargs):
        req = Util.createRequest(NOVAL_URL+'v2/%s/servers/%s/action' % (user['projectid'], kwargs.get('server_id')), 'POST',user) #500 error 48d8cd602577412c978f0184544e9e1c
        values = {
                   kwargs.get('action'): '' #"os-start"
                 }
        params = json.dumps(values)
        try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                code = response.code
                logger.debug(method_name+" code:" + str(code))
                return code
        except HTTPError, e:
                logging.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('Reason: not found the server')
                else:
                    raise APIError('Reason: '+str(e.message))
        except URLError, e:
                logging.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)
    return 'error', 'Input parameter error,can not start or stop server '


def delete_cache(instance_id, user):
    if instance_id is None:
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params=CACHE_SERVER_PARAMS).filter(
        category=CACHE_SERVER_CATEGORY)
    else:
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params=CACHE_SERVER_PARAMS).filter(
        category=CACHE_SERVER_CATEGORY).filter(content__icontains=instance_id)

    opcache[0].delete()

def update_cache(user, instance_id ,operate , new_instance = None):
    opcache = []
    if  operate == 'add':
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params=CACHE_SERVER_PARAMS).filter(category=CACHE_SERVER_CATEGORY)
    else:
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params=CACHE_SERVER_PARAMS).filter(category=CACHE_SERVER_CATEGORY).filter(content__icontains=instance_id)

    if opcache is not None and len(opcache) > 0  :  # update the cache table data
        obj = opcache[0].content
        if obj and len(obj):
            content = json.loads(obj)
            i = 0
            if operate == 'add':
                content['servers'].append(new_instance)
            else:
                for server_obj in content['servers']:
                    if server_obj.get('id') == instance_id:
                        i = i+1
                        if 'delete' == operate:
                            content['servers'].remove(server_obj)
                            break

                        elif 'update' == operate:
                            if new_instance is not None and len(new_instance) > 0:
                                for element in new_instance:
                                    element['visibility'] = 'xxx'
                            content['servers'][i] = new_instance
            opcache[0].content = json.dumps(content)
            opcache[0].save()


def delete_server(user,server_id):#163 {'tenant_id':tenant_id,'server_id':server_id}  #/v2/{tenant_id}/servers/{server_id}/action
    method_name = 'delete_server'
    req = Util.createRequest(NOVAL_URL+'v2/%s/servers/%s/action' % (user['projectid'], server_id), 'POST',user) #500 error 48d8cd602577412c978f0184544e9e1c
    values = {
                   "forceDelete": ''
             }
    params = json.dumps(values)
    try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            code = response.code
            logger.debug(method_name+" code:" + str(code))
            if code == 204 or code == 202:
                try:
                    update_cache(user,server_id, 'delete',None)
                except Exception, e:
                    print e.code
                    delete_cache(server_id, user)
            return code
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            if 404 == e.code:
                    raise APIError('Reason: not found the server')
            else:
                    raise APIError('Reason: '+str(e.message))
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)


def list_server_snapshot(user):#{'tenant_id':tenant_id}
    method_name = 'list_server_snapshot'
    req = Util.createRequest(NOVAL_URL+'v1.1/%s/os-snapshots' % user['projectid'], 'GET',user) #500 error 48d8cd602577412c978f0184544e9e1c
    try:
        response = urllib2.urlopen(req,  timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
    except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('Reason: not found the volume')
                else:
                    raise APIError('Reason: '+str(e.message))
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)



def create_server_snapshot(user,**kwargs):#841{'tenant_id':tenant_id, 'snaphot_content':snaphot_content }
    method_name = 'create_server_snapshot'
    # parameter = ('tenant_id')
    # if Util.validate_parameter(*parameter, **kwargs):
    req = Util.createRequest(NOVAL_URL+'v1.1/%s/os-snapshots' % user['projectid'], 'POST',user) #500 error 48d8cd602577412c978f0184544e9e1c
        # values = {
        #                 "snapshot": {
        #                     "display_name": "testing1126",
        #                     "volume_id": "2bd364d0-a3eb-4adf-be93-eeb6e583c987"
        #                 }
        #         }
    params = json.dumps(kwargs.get('snaphot_content'))
    try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
    except HTTPError, e:
                logger.error(method_name+" code:" + str(e.code)+" content:" + str(e.message))
                if 404 == e.code:
                    raise APIError('Reason: not found the snaphot')
                else:
                    raise APIError('Reason: '+str(e.message))
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)
    # return 'error', 'Input parameter error,can not create server snapshot'


def backup_server(user,**kwargs):#841{'tenant_id':tenant_id, 'snaphot_content':snaphot_content }
    method_name = 'backup_server'
    # parameter = ('tenant_id')
    # if Util.validate_parameter(*parameter, **kwargs):
    req = Util.createRequest(NOVAL_URL+'/v2/%s/servers/%s/action' %( user['projectid'],  '3b160a94-2050-4a72-811e-2df143b9d874'), 'POST',user) #500 error 48d8cd602577412c978f0184544e9e1c
        # values = {
        #                 "snapshot": {
        #                     "display_name": "testing1126",
        #                     "volume_id": "2bd364d0-a3eb-4adf-be93-eeb6e583c987"
        #                 }
        #         }
    params = json.dumps(kwargs)
    try:
            response = urllib2.urlopen(req, params, timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
    except HTTPError, e:
                logger.error(method_name+" code:" + str(e.code)+" content:" + str(e.message))
                if 404 == e.code:
                    raise APIError('Reason: not found the snaphot')
                else:
                    raise APIError('Reason: '+str(e.message))
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e.reason))
                raise APIError(' URLError: ', e.reason)

if __name__ == "__main__":
    #launch_server()
    values = {
            "os-migrateLive": {
                "host": "aaron-55",
                "block_migration": False,
                "disk_over_commit": False
                }
            }

    sersers={"server": {"name": "zzz",
                        "imageRef": "047ff440-2835-4129-b2a6-eaca1396695a",
                        "flavorRef": "1",
                        "return_reservation_id": "true",
                        "max_count": 1,
                        "available_zone": "nova",
                        "min_count": 1,
                        "networks": [{"uuid": "3891a9d6-9083-4bf3-8c99-034932c3e81c"}],
                        "metadata": {"My Server Name": "Apache1"}
                        }
             }
    sersers={"server": {"name": "portal12", "imageRef": "047ff440-2835-4129-b2a6-eaca1396695a", "flavorRef": "1", "return_reservation_id": "true", "max_count": 1, "available_zone": "nova", "min_count": 1, "networks": [{"uuid": "3891a9d6-9083-4bf3-8c99-034932c3e81c"}], "metadata": {"My Server Name": "Apache1"}}}
    sersers={'tenant_id': 'd04021d5a4144b4c9f579fdc1d1c2a9a', 'server': {'server': {'name': '1', 'imageRef': '047ff440-2835-4129-b2a6-eaca1396695a', 'flavorRef': '1', 'return_reservation_id': 'true', 'max_count': 1, 'available_zone': 'portal5', 'min_count': 1, 'networks': [{'uuid': '3891a9d6-9083-4bf3-8c99-034932c3e81c'}], 'metadata': {'My Server Name': 'Apache1'}}}}
    new_instance={"server": {"name": "nova", "imageRef": "fa2aea3a-109e-4790-9545-2b118721ec0d", "flavorRef": "1", "max_count": 1, "available_zone": "nova", "min_count": 1, "networks": [{"uuid": ["01db79e0-628f-4fb0-a483-c84f923b0728"]}]}}
    users={"username":"admin","password":"Abc12345","projectid":"d04021d5a4144b4c9f579fdc1d1c2a9a"}
    # launch_server(users,**sersers)
    delete_server(users,'4d9dceeb-f57d-4025-8f28-296b764c490b')
    server = {
        "server": {"name": "sddstest"}
    }
    update_server(users,'5ac35631-aca8-45e0-a574-ced0cc92f73b',server)
    user={'username': 'portal1', 'project_name': 'demo', 'projectid': '3cd084a024d64d0486920e28ec30a233', 'user_domain_name': 'Default', 'userid': 'd2370ed26c454733bb97abaec34db0d4', 'userroles': [{'id': '31fd1d2bb7e741218637e230c13df800', 'name': 'user'}], 'password': '123', 'project_domain_name': 'Default'}
    # user={'username': 'admin',   'project_name': 'admin', 'projectid': 'd04021d5a4144b4c9f579fdc1d1c2a9a', 'user_domain_name': 'Default', 'userid': '48d8cd602577412c978f0184544e9e1c', 'userroles': [{'id': '7461b89e471a41729769010cab38b71b', 'name': 'admin'}], 'password': 'Abc12345', 'project_domain_name': 'Default'}



