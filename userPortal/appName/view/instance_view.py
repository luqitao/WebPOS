# coding=utf-8
__author__ = 'aaron'
from appName.api import nova as nova_api
import json
import datetime
from django.utils.dateparse import parse_datetime
from appName.api.common.util import Util as Util
from appName.route import neutron_api as neutron_api
from image_view import Image

class Instance():
    def list_flavor(self,user):
        if user is not None and user.get('username') is not None:
            return  nova_api.list_flavor(user)

    def list_instance(self,user):
        server_list = nova_api.list_all_server(user)#获取某个租户下的所有的server instance
        image_obj = Image()
    	image_names = image_obj.list_all_image_names(user)
        instance_list = []
        if server_list is not None and (server_list[0] == 200 or server_list[0] == 203):
            servers = server_list[1]['servers']
            flavor_list = nova_api.list_flavor(user)
            for instance in servers:
                    server_new = {}
                    server_new['id'] = instance['id']
                    server_new['name'] = instance['name']
                    image_obj = instance['image']
                    image_obj = eval(json.dumps(image_obj))
                    image_id = ""
                    if image_obj is not None and len(image_obj) > 0:
                        for k, value in image_obj.items():
                            if k == 'id':
                                image_id = value
                                break
                        server_new['image'] = '---'
                       	for image_name in image_names:
                            if image_name['id'] == image_id:
                                 server_new['image'] = image_name['name']
                                 break

                    ip_address = ''
                    for k, v in instance['addresses'].items():
                        for value in v :
                            ip_address+=(value['addr'])
                            ip_address+=","

                    server_new['addresses'] = ip_address
                    if len(flavor_list) > 0:
                        for flavors in flavor_list:
                            if str(instance['flavor']['id']) == str(flavors['id']):
                                server_new['config'] = str(flavors['name'])
                                break

                    # server_new['config'] = 'config'
                    server_new['key_name'] = instance['key_name']

                    server_new['availability_zone'] = instance["OS-EXT-AZ:availability_zone"]
                    server_new['task'] = 'task'
                    # print 'OS-EXT-STS:power_state]',instance['OS-EXT-STS:power_state']
                    if instance['OS-EXT-STS:power_state'] == 1:
                        server_new['power_state'] = 'ACTIVE'
                        server_new['status'] = 'ACTIVE'
                    elif instance['OS-EXT-STS:power_state'] == 3:
                        server_new['power_state'] = 'Paused'
                        server_new['status'] = 'Paused'
                    elif instance['OS-EXT-STS:power_state'] == 4:
                        server_new['power_state'] = 'Shut Down'
                        server_new['status'] = 'Shutoff'
                    else:
                        server_new['power_state'] = instance['OS-EXT-STS:power_state']
                        server_new['status'] = instance['status']

                    now_time_eightHoursAgo = (datetime.datetime.now() - datetime.timedelta(hours = 8))
                    now_time=now_time_eightHoursAgo.strftime('%Y-%m-%d %H:%M:%S')
                    string = instance['created']
                    old_date = parse_datetime(string).date()
                    old_time = parse_datetime(string).time()
                    created_datetime = str(old_date)+" "+str(old_time)
                    display_time = Util.cal_time(created_datetime, now_time)
                    server_new['created'] = str(display_time)
                    instance_list.append(server_new)

        return instance_list


    def delete_instance(self, user,server_id):
        response = nova_api.delete_server(user,server_id)
        if response == 202 or response == 404:
            return {"Success":"OK"}
        else:
            return {"Error":"delete failed"}


    def launch_instance(self, user,server):
        instance_entity = json.dumps(server)
        instance_dict = eval(instance_entity)
        networks = instance_dict.get('networks')
        is_network = instance_dict.get('is_network')
        network_list = []
        instance_list = []
        if is_network:
            del is_network
            if len(networks) > 1 :
                for network in networks:
                    dictory = {}
                    dictory['uuid'] = network
                    network_list.append(dictory)
                instance_dict['networks'] = network_list

                instance_list =[{
                        'server':instance_dict
                    }]
            elif  len(networks) == 1 :
                instance_list =[{
                        'server':instance_dict
                    }]

        else:
            if len(networks) > 1:
                del instance_dict['networks']
                print 'instance_dict==',instance_dict
                instance_list = []

                for network_port in networks:
                    dictory = {}
                    list_dict = []
                    instance_dict = instance_dict.copy()
                    dictory['port'] = network_port
                    instance_dict['min_count'] = "1"
                    instance_dict['max_count'] = "1"
                    list_dict.append(dictory)

                    instance_dict['networks'] = list_dict
                    server_new = {
                        'server':instance_dict
                    }
                    instance_list.append(server_new)


            elif len(networks) == 1:
                    dictory = {}
                    dictory['port'] = networks[0]
                    network_list.append(dictory)
                    instance_dict['networks'] = network_list
                    instance_list =[{
                        'server':instance_dict
                    }]

        if len(instance_list) ==1:
            response = nova_api.launch_server(user,instance_list[0])
        else:
            response = nova_api.launch_server_by_thread(user,instance_list)

        if response[0] == 202:
            return {"Success":"OK"}
        else:
            return response[1]



    def operate_instance(self, user,**server):
        response = nova_api.operate_instance(user,**server)
        if response == 202:
            return {"Success":"OK"}
        else:
            return {"Error":"create failed"}

    def list_network_names(self, user):

        response = neutron_api.list_network(user,user.get('projectid'),False)
        if response[1] == 200:
             network_dir = response[0]
             network_list = network_dir['networks']
             network_array =[]
             for network_object in network_list:
                 network = {}
                 network['id'] = network_object['id']
                 network['name'] = network_object['name']
                 network_array.append(network)
             return network_array
        else:
             return {"Error":"list_network_names failed"}

    def list_network_port_names(self, user):
         network_port_list = nova_api.networkport_field_data(user)
         network_array =[]
         for network_object in network_port_list:
                 network = {}
                 network['id'] = network_object[0]
                 network['name'] = network_object[1]
                 network_array.append(network)
         return network_array
