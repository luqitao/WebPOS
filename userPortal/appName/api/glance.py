__author__ = 'aaron'
from common.util import Util
from urllib2 import URLError, HTTPError
import urllib2, json
import logging
from common.config import configs
from api_exception import APIError
import datetime
from ..models import Opcache
import os

GLANCE_URL = configs.get('glance')
TIME_OUT = configs.get('time_out')

#logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)



def show_image_detail_by_id(user,image_id):
    method_name = 'show_image_detail_by_id'
    req = Util.createRequest(GLANCE_URL+'v2/images/%s' % image_id, 'GET',user)
    code = 500
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            # logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
            return code, content
        else:
            logger.error(method_name+' Error code: '+response.code)
            return code, {"error":"error"}
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            if 404 == e.code:
                logger.error(method_name+'show image failed.Reason: not found the image')
            return e.code,  {"error":"error"}
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.code))
            return e.code,  {"error":"error"}
            # raise APIError(' URLError: ', e.reason)


def put_image_data(image_id, path,user):
    method_name = 'put_image_data'
    import requests
    # user = {"username":'admin',"password":'Abc12345'}
    code,x_token = Util._get_token(user)
    if code == 201:
        token = x_token['token']
        head = {
                "Content-Type": "application/octet-stream",
                "X-Auth-Token": token
               }
        # requests.head(head)
        url = GLANCE_URL+"v2/images/%s/file" % image_id
        if 'http:' in path:
            f = requests.get(path)
            try:
                r = requests.put(url, data=f, headers=head)
                return r.status_code
            except Exception as e:
                print e
        else:
            with open(path, 'rb') as f2:
                try:
                    print 'begin write data',f2
                    r = requests.put(url, data=f2, headers=head)
                    print 'statusCode',r.status_code
                    return r.status_code
                except Exception as e:
                    print e


def upload_image(user,**image):#1269 {'image':image}
    method_name = 'upload_image'
    req = Util.createRequest(GLANCE_URL+'v2/images', 'POST',user)
    fileName = None
    image_content = image.get('image')
    if image_content['fileName'] is not None:
         fileName = image_content['fileName']
         del image_content['fileName']

    try:
            response = urllib2.urlopen(req, json.dumps(image_content), timeout=TIME_OUT)
            obj = response.read()

            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                image_id = content['id']

                response_code = put_image_data(image_id,fileName,user)
                #add image to cache
                if response_code == 204:
                    try:
                        # image_content ={"protected": False, "name": "portal002", "container_format": "bare", "disk_format": "qcow2", "uri": "1", "visibility": "public", "description": "desc",
                        #          "fileName":"E:\portal_training\cirros-0.3.4-x86_64-disk.img"}
                        image_obj = {}

                        image_obj['name'] = image_content.get('name')
                        image_obj['description'] = image_content.get('description')
                        image_obj['container_format'] = image_content.get('container_format')
                        image_obj['protected'] = image_content.get('protected')
                        image_obj['disk_format'] = image_content.get('disk_format')
                        image_obj['visibility'] = image_content.get('visibility')
                        image_obj['owner'] = user.get('projectid')
                        image_obj['size'] = os.path.getsize(fileName)
                        now_time_eightHoursAgo = (datetime.datetime.now() - datetime.timedelta(hours = 8))
                        now_time = now_time_eightHoursAgo.strftime('%Y-%m-%d %H:%M:%S')
                        image_obj['created_at'] = str(now_time)
                        image_obj['id'] = image_id
                        update_cache(user,image_id, 'add',image_obj)
                    except Exception, e:
                        print e.code
                        delete_cache(image_id, user)
                else:
                    delete_cache(image_id, user)
                return response_code, content
            else:
                logger.error(method_name+' Error codexxx: '+str(response.code))
    except HTTPError, e:
                logger.error(method_name+' Error codexxzz: '+str(e.code))
                if 404 == e.code:
                    raise APIError('not found the image')
    except URLError, e:
                logger.error(method_name+' URLError: '+str(e))
                raise APIError(' URLError: ', e.reason)
    # else:
    #     return 'No image need to do the upload'


def delete_image(user,**image):#1265 {'image_id':imageId}
    method_name = 'delete_image'
    #You can delete an image in all status except deleted.
    # You must first set the 'protected' attribute to false (boolean) and then perform the delete.
    parameter = ['image_id']
    if Util.validate_parameter(*parameter, **image):
        image_id = image.get('image_id')
        req = Util.createRequest(GLANCE_URL+'v2/images/%s' % image_id, 'DELETE',user)
        try:
            response = urllib2.urlopen(req, timeout=TIME_OUT)
            code = response.code
            logger.debug(method_name+" code:" + str(code))
            # update cache failed, delete the whole cache table data
            try:
                update_cache(user,image_id, 'delete')
            except Exception, e:
                print e.code
                delete_cache(image_id, user)
            return code
        except HTTPError, e:
                logging.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError('not found the image')
        except URLError, e:
                logging.error(method_name+' URLError: '+str(e.code))
                raise APIError(' URLError: ', e.reason)
        except Exception ,e:
                logging.error(method_name+' Exception: '+str(e.code))
    return 'Input ImageId parameter error,No imageId can be deleted'


def delete_cache(image_id, user):
    opcache = Opcache.objects.filter(user=user.get('username')).filter(params='/v2/images').filter(
        category='list_image').filter(content__icontains=image_id)
    opcache[0].delete()


def update_cache(user,image_id, operate,new_image=None):
    opcache = []
    if  operate == 'add':
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params='/v2/images').filter(category='list_image')
    else:
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params='/v2/images').filter(category='list_image').filter(content__icontains=image_id)

    if opcache is not None and len(opcache) > 0 :  # update the cache table data
        obj = opcache[0].content
        if obj and len(obj):
            content = json.loads(obj)
            i = 0
            if operate == 'add':
                content['images'].append(new_image)
            else:
                for image_obj in content['images']:
                    if image_obj.get('id') == image_id:
                        i = i+1
                        if 'delete' == operate:
                            content['images'].remove(image_obj)
                            break

                        elif 'update' == operate:
                            if new_image is not None and len(new_image) > 0:
                                for element in new_image:
                                    key_name = element.get('path')
                                    if key_name == "/name":
                                        new_name = element.get('value')
                                        if new_name is not None and new_name > 0:
                                            image_obj['name'] = new_name
                                    if key_name == "/description":
                                        new_description = element.get('value')
                                        if new_description is not None and new_description > 0:
                                            image_obj['description'] = new_description

                                    if key_name == "/visibility":
                                        new_visibility = element.get('value')
                                        if new_visibility is not None and new_visibility > 0:
                                            image_obj['visibility'] = new_visibility

                                    if key_name == "/protected":
                                        new_protected = element.get('/value')
                                        if new_protected is not None and new_protected > 0:
                                            image_obj['protected'] = new_protected

                            content['images'][i] = image_obj


                        image_type = image_obj.get('image_type')
                        if image_type is None or image_type != 'snapshot':
                            image_obj['image_type'] = 'image'
            opcache[0].content = json.dumps(content)
            opcache[0].save()


def update_image(user,**image):#Attribute disk_format can be only replaced for a queued image
    method_name = 'update_image'
    parameter = ['image_id', 'image_content']
    if Util.validate_parameter(*parameter, **image):
        image_id = image.get('image_id')
        req = Util.createRequest(GLANCE_URL+'v2/images/%s' % image_id, 'PATCH', user, 'patch')
        try:
            image_content = image.get('image_content')
            response = urllib2.urlopen(req,  json.dumps(image_content), timeout=TIME_OUT)
            obj = response.read()

            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                if code == 200 or code == 204:
                    try:
                         update_cache(user,image_id,'update',image_content)
                    except Exception, e:
                        print e.code
                        delete_cache(image_id, user)

                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError(method_name+' failed.Reason: not found the image')
        except URLError, e:
                logger.error(method_name+' URLError: '+str(e.code))
                raise APIError(method_name+' URLError: '+str(e.reason))
    else:
        return 'Input ImageId parameter error,No image can be updated'


def share_image(user,**image):#1273 {'image_id':image_id,'members':members}
    method_name = 'share_image'
    parameter = ('image_id', 'members')
    if Util.validate_parameter(*parameter, **image):
        req = Util.createRequest(GLANCE_URL+"/v2/images/%s/members" % image.get('image_id'), 'POST')
        try:
            response = urllib2.urlopen(req, json.dumps(image.get('members')), timeout=TIME_OUT)
            obj = response.read()
            if obj and len(obj):
                content = json.loads(obj)
                code = response.code
                logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
                return code, content
            logger.error(method_name+' Error code: '+response.code)
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                raise APIError(method_name+' Error code: '+str(e.code))
        except URLError, e:
                logger.error(method_name+' URLError: '+str(e.code))
                raise APIError(method_name+' URLError: '+str(e.reason))
    return 'Input  parameter error,No image can be shared'


def download_image(image_dict):#1270 {'image_id':image_id, 'file_name':file_name}
    method_name = 'download_image'
    parameter = ['image_id', 'file_name']
    if Util.validate_parameter(*parameter, **image):
        req = Util.createRequest(GLANCE_URL+'v2/images/%s/file' % image.get('image_id'), 'GET', 'stream')
        try:
            response = urllib2.urlopen(req, timeout=TIME_OUT)
            with open(image.get('file_name'), 'wb') as f:
                while True:
                    tmp = response.read(1024)
                    if not tmp:
                        break
                    f.write(tmp)
            code = response.getcode()
            logger.debug(method_name+" code:" + str(code))
            return code
        except HTTPError, e:
                logger.error(method_name+' Error code: '+str(e.code))
                if 404 == e.code:
                    raise APIError(method_name+' failed.Reason: not found the image')
        except URLError, e:
                logger.error(method_name+' URLError: '+str(e.code))
                raise APIError(method_name+' URLError: '+str(e.reason))
    return 'Input  parameter error,No image can be downloaded'


def list_image(user,parameter='/v2/images'):#1258
    opcache = []
    opcache = Opcache.objects.filter(user=user.get('username')).filter(params=parameter).filter(category='list_image')
    if opcache is not None and len(opcache) >0:
    	obj = opcache[0].content
        if obj and len(obj):
            content = json.loads(obj)
            for image in content['images']:
                image_type = image.get('image_type')
                if image_type  is  None or image_type!='snapshot':
                    del image_type
                    image['image_type']='image'
            # logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
        return 200, content
    method_name = 'list_image'
    req = Util.createRequest(GLANCE_URL+parameter, 'GET',user)
    try:
        response = urllib2.urlopen(req, timeout=TIME_OUT)
        obj = response.read()
        o = Opcache()
        o.user = user.get('username')
        o.category = 'list_image'
	o.params = parameter
        o.content = obj 
        o.save()
        if obj and len(obj):
            content = json.loads(obj)
            code = response.code
            for image in content['images']:
                image_type = image.get('image_type')
                if image_type  is  None or image_type!='snapshot':
                    del image_type
                    image['image_type']='image'
            # logger.debug(method_name+" code:" + str(code)+" content:" + str(content))
        return code, content
    except HTTPError, e:
            logger.error(method_name+' Error code: '+str(e.code))
            if 404 == e.code:
                raise APIError(method_name+' failed.Reason: not found the image')
    except URLError, e:
            logger.error(method_name+' URLError: '+str(e.reason))
            raise APIError(method_name+' URLError: '+str(e.reason))

if __name__ == "__main__":
    image = {
                "id": "e7db3b45-8db7-47ad-8109-3fb55c2c24DD",
                'uri': "http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img",
                "name": "Aaron_Ubuntu_12.13",
                "tags": [
                    "ubuntu",
                    "quantal"
                ]
            }
    members = {
        "member": "48d8cd602577412c978f0184544e9e1c"
    }

    image = [{
        "path": "/visibility",
        "value": "public",
        "op": "replace"
        }]

    image = {
                # "id": "e7db3b45-8db7-47ad-8109-3fb55c2c24DD",
                'uri': "http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img",
                "name": "Aaron_Ubuntu_12.1",
                "visibility": "public",
                "disk_format": "qcow2"

                # "name": "Aaron_Ubuntu_12.13",
                # "tags": [
                #     "ubuntu",
                #     "quantal"
                # ]
            }
    # list_image()
    # image ={'disk_format': 'raw', 'name': 'testing_aaron', 'uri': 'http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img'}
    # image = { 'name': 'image_aaron', 'uri': 'http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img'}
    #print (upload_image(**{'image':image}))
    # delete_image(**{'image_id':'b928e239-3a2c-440f-8275-f61923b6b6a1'})
    image_content = [
        {
            "path": "/visibility",
            "value": "private",
            "op": "replace"
        },
        {
            "path": "/name",
            "value": "yezhiqinUpdate",
            "op": "replace"
        },
        {
                        "path": '/protected',
                        "value": False,
                        "op": "replace"
        },
        {
                        "path": '/disk_format',
                        "value": '1',
                        "op": "replace"
        }
    ]
    content = {'image_id':'37908001-5caf-4a48-825c-50c46a96851f', 'image_content':image_content}
    content= {'image_content':
                 [
                     {'path': '/visibility', 'value': 'public', 'op': 'replace'},
                     {'path': '/protected', 'value': True, 'op': 'replace'}
                 ],
                 'image_id': '37908001-5caf-4a48-825c-50c46a96851f'
            }
    content= {'image_content': [{'path': '/visibility',  'value': 'public', 'op': 'replace'},
                                {'path': '/protected',   'value': True,     'op': 'replace'},
                                {'path': '/disk_format', 'value': 'raw',    'op': 'replace'}
                                ],
              'image_id': '8d5a1142-8845-403a-a473-1c987f756ce6'}
    # content= {'image_content': [{'path': '/visibility', 'value': 'private', 'op': 'replace'},
    #                             {'path': '/protected', 'value': True, 'op': 'replace'},
    #                             {'path': '/disk_format', 'value': 3, 'op': 'replace'}],
    #             'image_id': '37908001-5caf-4a48-825c-50c46a96851f'}
    # update_image(**content)
    # print list_image()
    image = { "description": "test","disk_format": "raw", "name": "testing_image", "visibility": "public", "uri": "http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img"}
    image ={'description': 'desc111','disk_format': 'raw','container_format':'bare','name': '444testing',    'visibility': 'public', 'uri': 'yyy', 'protected': False}
    # image = {'protected': True, 'uri': 'zzz', 'name': 'testing-image', 'visibility': 'public', 'description': 'desc'}
    # image={'image_content': [{'path': '/name', 'value': 'xxx', 'op': 'replace'},
    #                          {'path': '/visibility', 'value': 'public', 'op': 'replace'},
    #                          {'path': '/protected', 'value': False, 'op': 'replace'}],
    #        'image_id': '1fb641f3-982d-4f8e-833e-47f6cb31803a'}
    # print update_image(**image)
    # print put_image_data('caea8d11-5a93-4781-ac68-0913f64427f7',r'E:\\portal_training\\cirros-0.3.4-x86_64-disk.img')
    # image = {'name': 'testing-image',  'uri': '1', 'visibility': 'private', 'protected': False, 'description': 'desc'}
    image = { "description": "test","disk_format": "qcow2",'container_format':'bare', "name": "testing_image222", "visibility": "public", "fileName": 'http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img'}
    image ={"protected": False, "name": "portal002", "container_format": "bare", "disk_format": "qcow2", "uri": "1", "visibility": "public", "description": "desc","fileName":"E:\portal_training\cirros-0.3.4-x86_64-disk.img"}
    user = {}
    user['username']='admin'
    user['password']='Abc12345'
    print upload_image(user,**{'image':image})
    # content =list_image(user)[1]['images']
    # print len(content)
