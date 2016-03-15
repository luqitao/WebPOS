# coding=utf-8
from appName.route.key_store_api import _getToken as getToken
from appName.route.test import *
from appName.route.cinder_api import *
from appName.route import ceilometer_api as ceilometer
from appName.api import nova
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import json
from api.common.util import Util
from appName.route import neutron_api as neutron_api

from .forms import Login
from view.project_view import Project
from view.instance_view import Instance
from view.image_view import Image
from view.user_view import User
REDIRECT_FIELD_NAME = 'next'
global total_image_list
total_image_list = []


def list_project(request):
    user = request.session['user']
    pro = Project()
    return HttpResponse(json.dumps(pro.list_project(user)), content_type="application/json")

def create_project(request):
    user = request.session['user']
    pro = Project()
    for key, item in request.POST.items():
            dictory = str(key)

    if dictory is not None and len(dictory) > 0:
        project = (eval(dictory)).get("project")
        if project.get('enabled')=='True':
           project['enabled']=True
        else:
           project['enabled']=False
        if project is not None and len(project) > 0:
            return HttpResponse(json.dumps(pro.create_project(user,**{"project":project})), content_type="application/json")

def delete_project(request):
   project_ids_str = request.POST.items()    # ['instanceIds']
   project_ids = []
   user = request.session['user']

   delete_resuslt = []
   pro = Project()
   for projects in project_ids_str:
        project_ids = eval(projects[0])
        if project_ids is not None and len(project_ids) > 0:
            for project_id in project_ids:
                result = pro.delete_project(user,project_id)

                delete_resuslt.append(result)#mutiple delete,should return all deleted result in one
   return HttpResponse(json.dumps(result), content_type="application/json")

def update_project(request):
    user = request.session['user']
    pro = Project()
    return HttpResponse(json.dumps(pro.update_project(user)), content_type="application/json")

def list_all_user_names(request):
    user_object = User()
    userobject= request.session['user']
    return HttpResponse(json.dumps(user_object.list_user_names(userobject)), content_type="application/json") #js can deal with it

def login(request):
    auth = {}
    if request.session.get('isLogined', False):#当已经登录
        return HttpResponseRedirect('/')
    elif request.method == 'POST':# 当提交表单时
        form = Login(request.POST) # form 包含提交的数据
        if form.is_valid():# 如果提交的数据合法
            auth['username'] = form.cleaned_data['username']
            auth['password'] = form.cleaned_data['password']
            code, response_info = Util._get_token(auth)
            if code == 201:
                request.session['isLogined'] = True
                request.session['token'] = response_info["token"]
                user = {}
                user["userid"]=response_info["userid"]
                user["userroles"]=response_info["userroles"]
                user["projectid"]=response_info["projectid"]
                user["user_domain_name"]=response_info["user_domain_name"]
                user["project_domain_name"]=response_info["project_domain_name"]
                user["project_name"]=response_info["project_name"]
                user["username"]= auth['username']
                user["password"]= auth['password']
                request.session['user'] = user
                return HttpResponseRedirect('/')
            else:
                request.session['isLogined'] = False
                return render(request, 'login.html', {'form': form, 'error':"用户名/密码错误"})
    else:# 当正常访问时
        form = Login()
    return render(request, 'login.html', {'form': form})

# from appName.route.auth.decorators import login_required
# @login_required(login_url="/login/")
def open_index(request):
    # print "request.session.get('isLogined', False):", request.session.get('isLogined', False)
    if request.session.get('isLogined', False):
        context = dict()
        username = request.session['user']['username']
        userroles = request.session['user']['userroles']
        user_role='false'
        for role in userroles:
            if role['name'] == 'admin':
                user_role = 'true'

        return render(request, "main.html", {'username':username,'user_role':user_role})
    else:
        return HttpResponseRedirect('/login/')

def logout(request):
    if request.session.get('isLogined', False):
        del request.session['isLogined']  #删除session
        del request.session['user']  #删除session
        del request.session['token']  #删除session
    return HttpResponseRedirect('/login/')


# cinder
def create_volume(request):
    directory = None
    for key, item in request.POST.items():
        directory = eval(key)
    if directory is not None and len(directory) > 0:
        response = createvolume(request, {"volume": directory})
        if response[1] == 202:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"create failed"}), content_type="application/json")

def update_volume(request):
    directory = None

    for key, item in request.POST.items():
        directory = json.loads(key)
    if directory is not None and len(directory) > 0:
        response = updatevolume(request, request.GET['id'], {"volume": directory[0]})
        if directory[0]['size'] > directory[1]:
            response_extend = extendvolume(request, request.GET['id'], {"os-extend":{"new_size":directory[0]['size']}})
        else:
            response_extend = ['',202]

        if response[1] == 200 and response_extend[1] == 202:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"update failed"}), content_type="application/json")

def delete_volume(request):
    directory = None
    for key, item in request.POST.items():
        directory = eval(key)
    if directory is not None and len(directory) > 0:
        response = deletevolume(request, directory)
        if response[1] == 202:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"delete failed"}), content_type="application/json")

def volumeinfo(request):
    user = request.session['user']
    return listvolume(request,user)

def attach_volume(request):
    directory = None
    for key, item in request.POST.items():
        directory = key
    if directory is not None and len(directory) > 0:
        response = attachvolume(request, directory, {'volumeAttachment': {'volumeId': request.GET['id']}})
        if response[1] == 200:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"attach failed"}), content_type="application/json")

def detach_volume(request):
    directory = None
    for key, item in request.POST.items():
        directory = json.loads(key)
    if directory is not None and len(directory) > 0:
        response = detachvolume(request, directory['server_id'], directory['id'])
        if response[1] == 202:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"attach failed"}), content_type="application/json")

def extend_volume(request):
    directory = None
    for key, item in request.POST.items():
        directory = eval(key)
    if directory is not None and len(directory) > 0:
        response = updatevolume(request, request.GET['id'], {"os-extend": directory})
        if response[1] == 200:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"create failed"}), content_type="application/json")

def create_snapshot(request):
    directory = None
    for key, item in request.POST.items():
        directory = eval(key)
    if directory is not None and len(directory) > 0:
        directory['volume_id'] = request.GET['id']

        response = createsnapshot(request, {"snapshot": directory})
        if response[1] == 202:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"create failed"}), content_type="application/json")

def snapshotinfo(request):
    return listsnapshot(request)

def update_snapshot(request):
    directory = None
    for key, item in request.POST.items():
        directory = json.loads(key)
    if directory is not None and len(directory) > 0:
        response = updatesnapshot(request, request.GET['id'], {"snapshot": directory})
        if response[1] == 200:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"update failed"}), content_type="application/json")

def delete_snapshot(request):
    directory = None
    for key, item in request.POST.items():
        directory = eval(key)
    if directory is not None and len(directory) > 0:
        response = deletesnapshot(request, directory)
        if response[1] == 202:
            return HttpResponse(json.dumps({"Success":"OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"delete failed"}), content_type="application/json")


# glance
# def image_index(request):
#     context = dict()
#     return render(request, "glance.html",context)




def open_instance(request):
    instance_obj = Instance()
    user = request.session['user']
    instance_list = instance_obj.list_instance(user)

    if instance_list is not None:
        return HttpResponse(json.dumps(instance_list), content_type="application/json")


def launch_instance(request):
    user = request.session['user']
    for key, item in request.POST.items():
        dictory = key
    result = json.loads(dictory)
    instance_entity = result.get('server')
    if instance_entity is not None:
        instance_obj = Instance()
        user = request.session['user']
        return HttpResponse(json.dumps(instance_obj.launch_instance(user,instance_entity)), content_type="application/json")


def list_flavor(request):
    # tenant_id = "d04021d5a4144b4c9f579fdc1d1c2a9a"
    user= request.session['user']
    instance_obj = Instance()
    flavor_list = instance_obj.list_flavor(user)

    return HttpResponse(json.dumps(flavor_list), content_type="application/json")


def terminate_instance(request):
    tenant_id = 'd04021d5a4144b4c9f579fdc1d1c2a9a'
    user= request.session['user']
    tenant_id=user['projectid']
    instance_ids_str = request.POST.items()    # ['instanceIds']
    instance_ids = []
    for k in instance_ids_str:
        instance_ids = eval(k[0])
    delete_resuslt = []
    if instance_ids is not None and len(instance_ids) > 0:
        instance_obj = Instance()
        for instance_id in instance_ids:
            result = instance_obj.delete_instance(user,instance_id)
            delete_resuslt.append(result)
    return HttpResponse(json.dumps(result), content_type="application/json")


def operate_instance(request):
    operate_parameter = request.GET   # ['instanceIds']
    operate_type = str(operate_parameter['operate_type'])
    instance_id = str(operate_parameter['id'])

    user= request.session['user']
    tenant_id=user['projectid']
    if operate_type is not None and len(operate_type) > 0:
        instance_obj = Instance()
        is_true = [(operate_type == 'PAUSE')]
        if operate_type == 'HARD' or operate_type == 'SOFT':
            instance_entity = {'tenant_id': tenant_id, 'server_id': instance_id,"operate_type": {
                        "reboot_type": {
                             "type": operate_type
                        }
                }}
        else:
            instance_entity = {'tenant_id': tenant_id, 'server_id': instance_id, "operate_type": {
                                    operate_type: 'null'
                                }
                               }

        reponse_result = instance_obj.operate_instance(user,**instance_entity)

        return HttpResponse(json.dumps(reponse_result), content_type="application/json")



def pause_instance(request):
    instance_ids_str = request.POST.items()    # ['instanceIds']

    user= request.session['user']

    if instance_ids_str is not None and len(instance_ids_str) > 0:
        instance_obj = Instance()
        if str(instance_ids_str).find(",") > 0:
            instance_ids = instance_ids_str.split(",")
            for instance_id in instance_ids:
                result = instance_obj.delete_instance(user,instance_id)
                return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponse(json.dumps(instance_obj.delete_instance(user, instance_ids_str)), content_type="application/json")


def list_network_names(request):
    instance_obj = Instance()
    user = request.session['user']
    return HttpResponse(json.dumps(instance_obj.list_network_names(user)),content_type="application/json")


def list_network_port_names(request):
    instance_obj = Instance()
    user = request.session['user']

    return HttpResponse(json.dumps(instance_obj.list_network_port_names(user)),content_type="application/json")


def list_image_names(request):

    imageObj = Image()
    user= request.session['user']


    return HttpResponse(json.dumps(imageObj.list_all_image_names(user)),content_type="application/json")



def update_instance(request):
    context = dict()

    return render(request, "instance.html", context)


def open_glance(request):
    image_obj = Image()
    user= request.session['user']
    new_image_list=[]
    image_list= image_obj.list_all_image(user)
    dicttory = dict()
    if image_list is not None and len(image_list) >0:
        # new_image_list.append("200")
        for img in image_list:
            if type(img)==dict:
                new_image_list.append(img)

    dicttory['images']=[]
    total_image = []
    for images in new_image_list:
        total_image = total_image+images['images']
    dicttory['images'].append(total_image)

    global total_image_list
    total_image_list = []
    return HttpResponse(json.dumps(dicttory),content_type="application/json") #js can deal with it
    # return render(request, "main.html",context) #html deal it with itself


def delete_image(request):
    image_ids_str = request.POST.items()    # ['instanceIds']
    image_ids = []
    for images in image_ids_str:
        image_ids = eval(images[0])
    delete_resuslt = []
    user = request.session['user']
    if image_ids is not None and len(image_ids) > 0:
        image_obj = Image()
        for image_id in image_ids:
            result = image_obj.delete_image({"image_id": image_id},user)
            delete_resuslt.append(result)#mutiple delete,should return all deleted result in one
    return HttpResponse(json.dumps(result), content_type="application/json")

def update_image(request):
    for key, item in request.POST.items():
        dictory = str(key)
    if dictory is not None and len(dictory) > 0:
        imageObj = Image()
        dictory_new = (eval(dictory)).get("image")
        image_content = []
        image_name = dictory_new.get('name')
        image_content.append({
                 "path": "/name",
                 "value": image_name,
                  "op": "replace"
        })

        image_description = dictory_new.get('description')
        image_content.append({
                 "path": "/description",
                 "value": image_description,
                  "op": "replace"
        })


        image_id = dictory_new.get('id')
        uri = dictory_new.get('uri')
        is_public = dictory_new.get('public')
        value = 'private'
        if is_public == 'True':
            value = 'public'
        image_content.append({
                 "path": "/visibility",
                 "value": value,
                  "op": "replace"
        })

        protecteds = dictory_new.get('protected')
        value = False
        if protecteds == 'True':
            value = True
        image_content.append({
                 "path": "/protected",
                 "value": value,
                  "op": "replace"
        })

        #Attribute disk_format can be only replaced for a queued image
        # disk_format = dictory_new.get('disk_format')
        #
        # image_content.append({
        #           "path": "/disk_format",
        #           "value": disk_format,
        #            "op": "replace"
        #  })



        # disk_format = dictory_new.get('disk_format')
        #
        # image_content.append({
        #           "path": "/disk_format",
        #           "value": disk_format,
        #            "op": "replace"
        #  })
        # address = dictory_new.get('address')
        # image_content.append({
        #           "path": "/uri",
        #           "value": address,
        #            "op": "replace"
        # })

        image_entity = {
                          'image_id': image_id,
                          'image_content': image_content
                        }
        print 'image_entity', image_entity
        #constructor the image object update format
        user= request.session['user']
    return HttpResponse(json.dumps(imageObj.update_image(user,**image_entity)), content_type="application/json")



def create_image(request):
    for key, item in request.POST.items():
            dictory = str(key)
    if dictory is not None and len(dictory) > 0:
        image_obj = Image()
        image_entity = (eval(dictory)).get("image")

        if image_entity['protected'] is None:
            image_entity['protected'] = False
        elif image_entity['protected'] == 'true':
            image_entity['protected'] = True
        else:
            image_entity['protected'] = False
        print 'create image_obj:',image_entity
        user= request.session['user']
        return HttpResponse(json.dumps(image_obj.create_image(user,**{'image': image_entity})), content_type="application/json")


def get_user(request):
    user_object = User()
    userobject= request.session['user']
    user_list = user_object.list_user(userobject)
    if user_list[0] == 200:
        user_list = user_list[1]
    return HttpResponse(json.dumps(user_list),content_type="application/json") #js can deal with it


def create_user(request):
    user_object = User()
    for key, item in request.POST.items():
        dictory = key
    user_entity = json.loads(dictory)
    user = request.session['user']
    return HttpResponse(json.dumps(user_object.create_user(user,**user_entity)), content_type="application/json")


def list_project_name(request):
    user_object = User()
    userobject= request.session['user']
    return HttpResponse(json.dumps(user_object.list_project_names(userobject)), content_type="application/json") #js can deal with it


def list_user_role(request):
    user_object = User()
    userobject= request.session['user']
    return HttpResponse(json.dumps(user_object.list_user_roles(userobject)), content_type="application/json") #js can deal with it


def update_user(request):
    pass


def delete_user(request):
   user_ids_str = request.POST.items()    # ['instanceIds']
   user_ids = []
   user = request.session['user']
   delete_resuslt = []

   user_obj = User()
   for users in user_ids_str:
        user_ids = eval(users[0])
        if user_ids is not None and len(user_ids) > 0:
            for user_id in user_ids:
                result = user_obj.delete_user(user,user_id)
                delete_resuslt.append(result)#mutiple delete,should return all deleted result in one
   return HttpResponse(json.dumps(result), content_type="application/json")



# ceilometer
def ceilometers_get_meters(request):
    context = ceilometer.list_meter()
    return HttpResponse(context)

def ceilometers_get_alarms(request):
    context = ceilometer.list_alarms()
    return HttpResponse(context)

def ceilometer_total(request):
    usage = []
    # Get meter name and project_id
    try:
        meters = json.loads(ceilometer.list_meter())
    except:
        return HttpResponse('[]')
    for i in meters[0:30]:
        tmp = dict()
        tmp['name'] = i['name']
        tmp['project_id'] = i['project_id']
        usage.append(tmp)
    date_from = request.GET['from']                    # Get time of user selected
    # date_to = request.GET['to']
    for i in usage:                    # According time to get meter statistics
        q = [{"field" : "timestamp", "op" : "ge", "value" : date_from, "type" : "None"}]
        static = ceilometer.show_meter_statistics(i['name'], q)
        static = json.loads(static)
        if len(static) is 0:
            continue
        else:
            i['sum'] = static[0]['sum']
            i['avg'] = static[0]['avg']
            i['unit'] = static[0]['unit']
    result = json.dumps(usage)
    return HttpResponse(result)

def getInformation(request):
    info = []
    user= request.session['user']
    server_list = nova.list_all_server(user)
    servers = server_list[1]['servers']
    for instance in servers:
        tmp_info = {'id' : instance['id'], 'name' : instance['name'],'ip' : [], 'NetInRate' : 0, 'NetOutRate' : 0,
                    'CpuUtil' : 0, 'Memory' : 0, 'MemoryUsage' : 0, 'DiskReadRate' : 0, 'DiskWriteRate' : 0}
        ip_address = []
        for v in instance['addresses'].values():
            for value in v :
                ip_address.append(value['addr'])
        tmp_info['ip'] = ip_address
        info.append(tmp_info)
    netGet = {'network.incoming.bytes.rate' : [], 'network.outgoing.bytes.rate' : []}
    for net in netGet.keys():
        netGet[net] = json.loads(ceilometer.show_meter_statistics(net, [], 'resource_id'))
    for instance in info:
        for i in netGet['network.incoming.bytes.rate']:
            if instance['id'] in i['groupby']['resource_id']:
                instance['NetInRate'] = i['avg']
                break
        for i in netGet['network.outgoing.bytes.rate']:
            if instance['id'] in i['groupby']['resource_id']:
                instance['NetOutRate'] = i['avg']
                break
    for instance in info:
        q = [{'field':'resource_id', 'op':'eq', 'value':instance['id']}]
        meterinfo = {'cpu_util' : 'CpuUtil', 'memory' : 'Memory', 'memory.usage' : 'MemoryUsage',
                     'disk.read.bytes.rate' : 'DiskReadRate', 'disk.write.bytes.rate' : 'DiskWriteRate',}
        for k, v in meterinfo.items():
            meters = json.loads(ceilometer.show_meter_statistics(k, q))
            if meters:
                instance[v] = meters[0]['avg']
            else:
                instance[v] = 0
    instanceinfo = json.dumps(info)
    return HttpResponse(instanceinfo)

# neutron
class neutron_info(object):

    @classmethod
    def list_networks(self, request):
        user = request.session['user']
        context = neutron_api.list_network(user,user.get('projectid'),False)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def delete_networks(self, request):
        if request.META.get('REQUEST_METHOD', '') == 'DELETE':
            path = json.dumps(request.META.get('PATH_INFO', ''))
            string = '/neutron/delete_networks/'
            if path is not None and len(str(path)) > 0 and (str(path)).find(string) != -1:
                parameters = {"network_id": path[len(string)+1:-1]}
                return HttpResponse(json.dumps(neutron_api.delete_network(parameters.get("network_id"))),
                                    content_type="application/json")
            else:
                print 'Parameter not correct'

    # @classmethod
    # def create_network(self, **network):
    #     response = neutron_api.create_network(**network)
    #     if response[0] == 201:
    #         return {"Success": "OK"}
    #     else:
    #         return {"Error": "create failed"}


    @classmethod
    def create_network(self,request):
        # print request.POST.items()
        for key, item in request.POST.items():
                dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict = eval(dictory).get('network')
            nw_name = dict.get('name')
            nw_tenantid = dict.get('project')
            # nw_shared = dict.get('shared')
            # nw_state = dict.get('state')
            nw_shared = 'true' if dict.get('shared') == 'YES' else 'false'
            nw_state = 'true' if dict.get('state') == 'UP' else 'false'
            nw_external = 'true' if dict.get('external') == 'YES' else 'false'

            # print nw_name, nw_shared, nw_state
            nw_entity = {"name": nw_name, "shared": nw_shared, "admin_state_up": nw_state,
                         "router:external": nw_external, "tenant_id": nw_tenantid}

            return HttpResponse(json.dumps(neutron_api.create_network(**{'network': nw_entity})),
                                content_type="application/json")

    @classmethod
    def update_network(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict = eval(dictory).get('network')
            nw_id = dict.get('id')
            nw_name = dict.get('name')
            # nw_shared = 'true' if dict.get('shared') == 'YES' else 'false'
            nw_state = 'true' if dict.get('state') == 'UP' else 'false'

            nw_entity = {"name": nw_name, "admin_state_up": nw_state}

            return HttpResponse(json.dumps(neutron_api.update_network(nw_id, **{'network': nw_entity})),
                                content_type="application/json")

    @classmethod
    def list_projects(self,request):
        project_list = neutron_api.list_project()
        projects = project_list[0]
        if project_list[1] == 200:
            project_name_list = []
            for project in projects[0]:
                if len(project['name']) < 200:
                    map = {}
                    map['id'] = project['id']
                    map['name'] = project['name']
                    project_name_list.append(map)

            return HttpResponse(json.dumps(project_name_list), content_type="application/json")

    @classmethod
    def create_subnet(self,request):
        # print request.POST.items()
        for key, item in request.POST.items():
                dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_net = eval(dictory).get('network')
            dict_sub = eval(dictory).get('subnet')
            enable_dhcp = 'true' if dict_sub.get("enable_dhcp") == 'YES' else 'false'
            allocation_pools = []
            dns_nameservers = []
            # pools = dict_sub.get("allocation_pools").split(',')

            if dict_sub.get("allocation_pools") != None:
                pools = dict_sub.get("allocation_pools").split(',')
                allocation_pools = [{"start": pools[0],"end":pools[1]}]
            if dict_sub.get("dns_nameservers") != None:
                dns_nameservers = [dict_sub.get("dns_nameservers")]


            # print "name", dict_net.get('name')
            # nw_state = 'true' if dict_net.get('state') == 'UP' else 'false'
            # print pools,type(pools),pools[0]
            # print allocation_pools

            subnet_info = {"name": dict_net.get('name'), "network_id": dict_net.get('id'),
                           "tenant_id": dict_net.get('tenant_id'),
                           "cidr": dict_sub.get('address'), "name": dict_sub.get("name"),
                           "enable_dhcp": enable_dhcp, "dns_nameservers": dns_nameservers,
                           "allocation_pools": allocation_pools,
                           "gateway_ip": dict_sub.get("gateway"), "ip_version": dict_sub.get("version")
                           }

            # print subnet_info
            return HttpResponse(json.dumps(neutron_api.create_subnet(**{'subnet': subnet_info})),
                                content_type="application/json")
    @classmethod
    def list_subnets(self,request):
        context = neutron_api.list_subnet()
        return HttpResponse(json.dumps(context[0]), content_type="application/json")


    @classmethod
    def list_floatingip(self,request):
        context = neutron_api.list_floatingip('DOWN')
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def allocate_floatingip(self, request):
        # print request.POST.items()
        for key, item in request.POST.items():
                dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            ipinfo = eval(dictory).get('ipinfo')


            # print dict_sub
            # print dict_net
            # print "name", dict_net.get('name')
            # nw_state = 'true' if dict_net.get('state') == 'UP' else 'false'
            # print nw_state

            # return HttpResponse(json.dumps(neutron_api.create_subnet(**{'subnet': subnet_info})),
            #                     content_type="application/json")

    @classmethod
    def list_pool(self,request):
        context = neutron_api.list_pool()
        return HttpResponse(json.dumps(context[0]), content_type="application/json")


    @classmethod
    def list_routers(self,request):
        context = neutron_api.list_routers('d04021d5a4144b4c9f579fdc1d1c2a9a')
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def list_extnet(self,request):
        user = request.session['user']
        context = neutron_api.list_network(user,'', True)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def create_router(self, request):
        # print request.POST.items()
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_router = eval(dictory).get('routerinfo')
            admin_state_up = 'True' if dict_router.get('state') == 'UP' else 'False'
            router_info = {"name": dict_router.get('name'), "external_gateway_info": {
                           "network_id": dict_router.get('network')}, "admin_state_up":admin_state_up}

            return HttpResponse(json.dumps(neutron_api.create_router(**{'router': router_info})),
                                content_type="application/json")

    @classmethod
    def add_interface(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_inf = eval(dictory).get('interface')

            return HttpResponse(json.dumps(neutron_api.add_interface(dict_inf.get("id"), **{'subnet_id': dict_inf.get('subnet')})),
                                content_type="application/json")

    @classmethod
    def list_ports(self,request):
        context = neutron_api.list_ports()
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def associate_ip(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_inf = eval(dictory).get('info')

            return HttpResponse(json.dumps(neutron_api.update_floatingip(dict_inf.get("ip"), **{'floatingip': {"port_id": dict_inf.get('port')}})),
                                content_type="application/json")


    @classmethod
    def disassociate_ip(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_inf = eval(dictory).get('info')

            return HttpResponse(json.dumps(neutron_api.update_floatingip(dict_inf.get("ip"), **{'floatingip': {"port_id": None}})),
                                content_type="application/json")


    @classmethod
    def delete_router(self, request):
        if request.META.get('REQUEST_METHOD', '') == 'DELETE':
            path = json.dumps(request.META.get('PATH_INFO', ''))
            string = '/router/delete_router/'
            if path is not None and len(str(path)) > 0 and (str(path)).find(string) != -1:
                parameters = {"router_id": path[len(string)+1:-1]}
                return HttpResponse(json.dumps(neutron_api.delete_router(parameters.get("router_id"))),
                                    content_type="application/json")
            else:
                print 'Parameter not correct'


    @classmethod
    def update_router(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict = eval(dictory).get('router')
            router_id = dict.get('id')
            router_name = dict.get('name')
            # nw_shared = 'true' if dict.get('shared') == 'YES' else 'false'
            router_state = 'true' if dict.get('state') == 'UP' else 'false'
            router_entity = {"name": router_name, "admin_state_up": router_state}

            return HttpResponse(json.dumps(neutron_api.update_router(router_id, **{'router': router_entity})),
                                content_type="application/json")

    @classmethod
    def list_groups(self,request):
        context = neutron_api.list_securitygroup()
        # json.dump(context, open('list_network.json', 'w'), indent=4)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def create_group(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_group = eval(dictory).get('groupinfo')
            group_info = {"name": dict_group.get('name'), "description": dict_group.get('description')}

            return HttpResponse(json.dumps(neutron_api.create_securitygroup(**{'security_group': group_info})),
                                content_type="application/json")

    @classmethod
    def delete_group(self, request):
        if request.META.get('REQUEST_METHOD', '') == 'DELETE':
            path = json.dumps(request.META.get('PATH_INFO', ''))

            string = '/securitygroup/delete_group/'
            if path is not None and len(str(path)) > 0 and (str(path)).find(string) != -1:
                parameters = {"router_id": path[len(string)+1:-1]}
                return HttpResponse(json.dumps(neutron_api.delete_securitygroup(parameters.get("router_id"))),
                                    content_type="application/json")
            else:
                print 'Parameter not correct'


    @classmethod
    def update_group(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict = eval(dictory).get('group')
            group_id = dict.get('id')
            group_name = dict.get('name')
            group_des = dict.get('description')
            group_entity = {"name": group_name, "description": group_des}
            # print 'group_entity', group_entity
            return HttpResponse(json.dumps(neutron_api.update_securitygroup(group_id, **{'security_group': group_entity})),
                                content_type="application/json")


    @classmethod
    def add_grouprules(self, request):
        for key, item in request.POST.items():
            dictory = key.encode("utf-8")

        if dictory is not None and len(dictory) > 0:
            dict_inf = eval(dictory).get('info')
            list_port = eval(dictory).get('protocal')
            # print list_port, dict_inf

            sgroup_direction = dict_inf.get('direction')
            sgroup_id = dict_inf.get('id')
            if dict_inf.has_key('prefix'):
                remote_ip_prefix = dict_inf.get('prefix')
            else:
                remote_ip_prefix = None

            rule_list = []
            for port in list_port:
                str = port.split(':')
                protocol = str[0]
                range = str[1].split('-')

                range_min = range[0]
                range_max = range[1]

                if range_min == 0:
                    range_min = None
                    range_max = None

                rule_enty = {'security_group_rule': {
                                     'security_group_id': sgroup_id,
                                     'direction': sgroup_direction,
                                     'remote_ip_prefix': remote_ip_prefix,
                                     'protocol':protocol,
                                     'port_range_min': range_min,
                                     'port_range_max': range_max
                                  }
                             }

                rule_list.append(rule_enty)

            return HttpResponse(json.dumps(neutron_api.create_secgourprules(rule_list)),
                                content_type="application/json")

    @classmethod
    def list_lbpools(self,request):
        context = neutron_api.list_lbpools()
        # json.dump(context, open('list_lbpools.json', 'w'), indent=4)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def add_lbpool(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_pool = eval(dictory).get('info')

            return HttpResponse(json.dumps(neutron_api.create_lbpool(**{'pool': dict_pool})),
                                content_type="application/json")

    @classmethod
    def update_lbpool(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict = eval(dictory).get('pool')
            pool_id = dict.get('id')
            pool_name = dict.get('name')
            pool_state = 'true' if dict.get('state') == 'UP' else 'false'
            pool_method = dict.get('method')
            pool_description = dict.get('description')
            pool_entity = {"name": pool_name, "admin_state_up": pool_state,"lb_method":pool_method,
                           "description": pool_description}

            return HttpResponse(json.dumps(neutron_api.update_lbpool(pool_id, **{'pool': pool_entity})),
                                content_type="application/json")

    @classmethod
    def delete_lbpool(self, request):
        if request.META.get('REQUEST_METHOD', '') == 'DELETE':
            path = json.dumps(request.META.get('PATH_INFO', ''))
            string = '/loadbalancer/delete_lbpool/'
            if path is not None and len(str(path)) > 0 and (str(path)).find(string) != -1:
                parameters = {"pool_id": path[len(string)+1:-1]}
                return HttpResponse(json.dumps(neutron_api.delete_lbpool(parameters.get("pool_id"))),
                                    content_type="application/json")
            else:
                print 'Parameter not correct'

    @classmethod
    def list_monitors(self,request):
        context = neutron_api.list_lbmonitors()
        # json.dump(context, open('list_lbpools.json', 'w'), indent=4)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def associate_monitor(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_pool = eval(dictory).get('pool')
            return HttpResponse(json.dumps(neutron_api.associate_monitor(dict_pool.get("id"),
                                **{'health_monitor': {"id": dict_pool.get('monitor')}})),
                                content_type="application/json")

    @classmethod
    def disassociate_monitor(self, request):
        if request.META.get('REQUEST_METHOD', '') == 'DELETE':
            path = json.dumps(request.META.get('PATH_INFO', ''))
            string = '/loadbalancer/disassociate_monitor/'
            if path is not None and len(str(path)) > 0 and (str(path)).find(string) != -1:
                parameters = path[len(string)+1:-1]
                ids = parameters.split('&&')
                return HttpResponse(json.dumps(neutron_api.disassociate_monitor(ids[0],ids[1])),
                                    content_type="application/json")

    @classmethod
    def add_lbmonitor(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_monitor = eval(dictory).get('info')

            return HttpResponse(json.dumps(neutron_api.add_lbmonitor(**{"health_monitor": dict_monitor})),
                                content_type="application/json")

    @classmethod
    def add_lbmember(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_member = eval(dictory).get('info')
            pool_id = dict_member.get('pool')
            addresses = dict_member.get('member')[0]

            member_entity = {'admin_state_up': dict_member.get('admin_state_up'), 'address': addresses, 'protocol_port': dict_member.get('port'),
                             'weight': dict_member.get('weight'), 'pool_id': pool_id}
            return HttpResponse(json.dumps(neutron_api.create_lbmember(**{'member': member_entity})),
                                content_type="application/json")

    @classmethod
    def list_firewall(self,request):
        context = neutron_api.list_firewalls()
        # json.dump(context, open('list_firewall.json', 'w'), indent=4)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def list_policy(self,request):
        context = neutron_api.list_policys()
        # json.dump(context, open('list_policys.json', 'w'), indent=4)
        return HttpResponse(json.dumps(context[0]), content_type="application/json")


    @classmethod
    def create_firewall(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_fw = eval(dictory).get('fwinfo')
            router_ids = []
            if dict_fw.get("router") != None:
                router_ids = [dict_fw.get("router")]
            fw_state = 'true' if dict_fw.get('state') == 'UP' else 'false'

            fw_info = {"name": dict_fw.get('name'), "description": dict_fw.get('description'),
                       "firewall_policy_id": dict_fw.get('policy'), "router_ids":router_ids,
                       "admin_state_up": fw_state}

            # print fw_info
            return HttpResponse(json.dumps(neutron_api.create_firewall(**{'firewall': fw_info})),
                                content_type="application/json")

    @classmethod
    def delete_firewall(self, request):
        if request.META.get('REQUEST_METHOD', '') == 'DELETE':
            path = json.dumps(request.META.get('PATH_INFO', ''))
            string = '/firewall/delete_firewall/'
            if path is not None and len(str(path)) > 0 and (str(path)).find(string) != -1:
                parameters = {"firewall_id": path[len(string)+1:-1]}
                return HttpResponse(json.dumps(neutron_api.delete_firewall(parameters.get("firewall_id"))),
                                    content_type="application/json")
            else:
                print 'Parameter not correct'


    @classmethod
    def list_fwrule(self,request):
        context = neutron_api.list_fwrules()
        return HttpResponse(json.dumps(context[0]), content_type="application/json")

    @classmethod
    def add_policy(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_policy = eval(dictory).get('info')
            policy_rules = []
            if dict_policy.get("rule") != None:
                policy_rules = [dict_policy.get("rule")]
            policy_shared = 'true' if dict_policy.get('shared') == 'YES' else 'false'
            policy_audited = 'true' if dict_policy.get('audited') == 'YES' else 'false'

            policy_info = {"name": dict_policy.get('name'), "description": dict_policy.get('description'),
                       "firewall_rules": policy_rules, "shared":policy_shared,
                       "audited": policy_audited}

            return HttpResponse(json.dumps(neutron_api.create_fwpolicy(**{'firewall_policy': policy_info})),
                                content_type="application/json")

    @classmethod
    def add_fwrule(self, request):
        for key, item in request.POST.items():
            dictory = str(key)

        if dictory is not None and len(dictory) > 0:
            dict_rule = eval(dictory).get('info')

            rule = (eval(dictory)).get("info")

            # source_ip_address = None
            # if dict_rule.get("sourceip") != None:
            #     source_ip_address = dict_rule.get("sourceip")
            #
            # source_port = None
            # if dict_rule.get("sourceport") != None:
            #     source_port = dict_rule.get("sourceport")
            #
            # destination_ip_address = None
            # if dict_rule.get("destinationip") != None:
            #     destination_ip_address = dict_rule.get("destinationip")
            #
            # destination_port = None
            # if dict_rule.get("destinationport") != None:
            #     destination_port = dict_rule.get("destinationport")
            #
            # rule_info = {"name": dict_rule.get('name'), "description": dict_rule.get('description'),
            #                "protocol": dict_rule.get('protocol'),"action": dict_rule.get('action'),
            #                "source_ip_address": source_ip_address,"source_port": source_port,
            #                "destination_ip_address": destination_ip_address,"destination_port":destination_port
            #                # "shared": dict_rule.get('shared'), "enabled": dict_rule.get('shared')
            #                }
            #
            # print rule_info
            return HttpResponse(json.dumps(neutron_api.create_fwrule(**{'firewall_rule': rule})),
                                content_type="application/json")

    @classmethod
    def update_firewall(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict_fw = eval(dictory).get('firewall')
            fw_id = dict_fw.get('id')
            fw_name = dict_fw.get('name')
            fw_des = dict_fw.get('description')
            fw_state = 'true' if dict_fw.get('state') == 'UP' else 'false'
            fw_entity = {"name": fw_name, "description": fw_des, "admin_state_up": fw_state,
                         "firewall_policy_id": dict_fw.get('policy')
                         }
            # print 'group_entity', group_entity
            return HttpResponse(json.dumps(neutron_api.update_firewall(fw_id, **{'firewall': fw_entity})),
                                content_type="application/json")

    @classmethod
    def add_router_to_fw(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict_fw = eval(dictory).get('firewall')
            fw_id = dict_fw.get('id')
            fw_routerids = dict_fw.get('router_ids')
            fw_routerids.append(dict_fw.get('router'))

            fw_entity = {"router_ids": fw_routerids}

            return HttpResponse(json.dumps(neutron_api.update_firewall(fw_id, **{'firewall': fw_entity})),
                                content_type="application/json")

    @classmethod
    def remove_router_to_fw(self,request):
        for key, item in request.POST.items():
            dictory = str(key)
        if dictory is not None and len(dictory) > 0:
            dict_fw = eval(dictory).get('firewall')
            fw_id = dict_fw.get('id')
            fw_routerids = dict_fw.get('router_ids')
            fw_routerids = filter(lambda x: x != dict_fw.get('router'), fw_routerids)

            fw_entity = {"router_ids": fw_routerids}

            # print 'group_entity', group_entity
            return HttpResponse(json.dumps(neutron_api.update_firewall(fw_id, **{'firewall': fw_entity})),
                                content_type="application/json")

def get_console_url(request):
    #print "##########get_console_url##########"
    CONSOLES = {"vnc":{"os-getVNCConsole": {"type": "novnc"}},"spice":{"os-getSPICEConsole": {"type": "spice-html5"}},"rdp":{"os-getRDPConsole": {"type": "rdp-html5"}},"serial":{"os-getSerialConsole": {"type": "serial"}}}

    #print "request:",request.POST
    if request.GET['id']:
        for con_type, api_body in CONSOLES.iteritems():

            try :
                #print "#######try########",con_type, api_body
                response = getconsole(request, request.GET['id'], api_body)
                #print "#######response########",response
            except :
                continue
            if response[1] == 200:
                urldate = eval(response[0])['console']['url']
                return HttpResponse(json.dumps({"Success":"OK" , "Date":urldate}), content_type="application/json")
    return HttpResponse(json.dumps({"Error":"update failed"}), content_type="application/json")

