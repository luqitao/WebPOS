import urllib2
import json
from urllib2 import URLError, HTTPError
from appName.api.common.config import configs
from appName.api import nova as nova_api
# from datetime import datetime
from ..models import Opcache

service_ip = 'http://10.89.151.12:'
neutron_url = service_ip + '9696'
NOVAL_URL = configs.get('nova')

# urlib2 get token
def gettoken_new():
    data = {
                "auth": {
                    "identity": {
                        "methods": [
                            "password"
                        ],
                        "password": {
                            "user": {
                                "domain": {
                                    "name": "Default"
                                },
                                "name": "yzq",
                                "password": "yzq"
                            }
                        }
                    },
                    "scope": {
                        "project": {
                            "domain": {
                                "name": "Default"
                            },
                            "name": "admin"
                        }
                    }
                }
            }

    req = urllib2.Request(service_ip + '35357/v3/auth/tokens')
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib2.urlopen(req, json.dumps(data))
        return response.headers['X-Subject-Token']
    except HTTPError:
        raise 'not found server'


# 15.2.2  create network
def create_network(**network):
    # data = {
    #             "network": {
    #                 "name": "tcx",
    #                 "admin_state_up": "true"
    #             }
    #         }
    req = urllib2.Request(neutron_url+'/v2.0/networks')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(network))
        code = response.getcode()
        content = json.loads(response.read())

        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'
    except URLError, e:
        raise 'URLError', e.reason


# 12.2.5 update network
def update_network(id, **network):
    # data = {
    #             "network": {
    #                 "name": "tcx_update_update",
    #                 "shared": "true"
    #             }
    #         }

    req = urllib2.Request(neutron_url+'/v2.0/networks/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(network))
        code = response.getcode()
        content = json.loads(response.read())

        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'


# 15.2.1 list network  parameter:network name
def list_all_network():

    req = urllib2.Request(neutron_url+'/v2.0/networks')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        # networklist = content['networks']
        #
        # for network in networklist:
        #     for k, v in network.iteritems():
        #         pass
                # if k == 'admin_state_up':
                #     network['admin_state_up'] = 'UP' if network['admin_state_up'] == 'true' else 'DOWN'
                # if k == 'shared':
                #     network['shared'] = 'YES' if network['shared'] == 'true' else 'NO'

        return content, code

        # network_id = ''
        # if name != '':
        #     for network in networklist:
        #         for k, v in network.iteritems():
        #             if v == name:
        #                 network_id = network.get('id', '')
        #                 break
        #     return network_id
    except HTTPError:
        raise 'not found server'


# 15.2.1 list network  parameter:project id
def list_network(user,projectid, isext):

    req = urllib2.Request(neutron_url+'/v2.0/networks')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    # json.dump(user, open('user.json', 'w'), indent=4)

    try:
        opcache = []
        params = ''
	if isext is False :
           params = " ".join((projectid, "False"))
        else:
           params = " ".join((projectid, "True"))
        opcache = Opcache.objects.filter(user=user.get('username')).filter(params=params).filter(category='list_network')
	content = ''
        if opcache is not None and len(opcache) >0:
            code = 200
            data = opcache[0].content
            content = json.loads(data)
	else:
            response = urllib2.urlopen(req)
            code = response.getcode()
            data = response.read();
            content = json.loads(data)
            if code == 200:
                o = Opcache()
                o.user = user
                o.category = 'list_network'
                o.params = params
                o.content = data
                o.save()
        networklist = content['networks']

        syslist = []
        newlist = []
        extlist = []
        for network in networklist:
            if(len(network['tenant_id']) != 0):
                syslist.append(network)
            if(len(projectid) != 0):
                if network['tenant_id'] == projectid or network['shared']:
                    newlist.append(network)
            if network['router:external']:
                extlist.append(network)

            # for k, v in network.iteritems():
                # if k == 'admin_state_up':
                #     print network['admin_state_up']
                #     print network['admin_state_up'] == "True"
                #     network['admin_state_up'] = 'UP' if network['admin_state_up'] == 'True' else 'DOWN'
                # if k == 'shared':
                #     network['shared']
                #     network['shared'] = 'YES' if network['shared'] == 'True' else 'NO'
        content = {"networks": syslist}
        if (len(projectid) != 0):
            content = {"networks": newlist}
        if isext:
            content = {"networks": extlist}

        # json.dump(content, open('network.json', 'w'), indent=4)
        return content, code

        # network_id = ''
        # if name != '':
        #     for network in networklist:
        #         for k, v in network.iteritems():
        #             if v == name:
        #                 network_id = network.get('id', '')
        #                 break
        #     return network_id
    except HTTPError:
        raise 'not found server'



# # 15.2.1 list network  parameter: field, value
# def list_network(field,value):
#
#     req = urllib2.Request(neutron_url+'/v2.0/networks')
#     req.add_header('Content-Type', 'application/json')
#     req.add_header('X-Auth-Token', gettoken_new())
#
#     try:
#         response = urllib2.urlopen(req)
#         code = response.getcode()
#         content = json.loads(response.read())
#         networklist = content['networks']
#
#         print len(networklist)
#         newlist = []
#         for network in networklist:
#             if(len(value) != 0):
#                     print len(network['tenant_id'])
#                     if network['tenant_id'] == value:
#                         newlist.append(network)
#
#             # for k, v in network.iteritems():
#                 # if k == 'admin_state_up':
#                 #     print network['admin_state_up']
#                 #     print network['admin_state_up'] == "True"
#                 #     network['admin_state_up'] = 'UP' if network['admin_state_up'] == 'True' else 'DOWN'
#                 # if k == 'shared':
#                 #     network['shared']
#                 #     network['shared'] = 'YES' if network['shared'] == 'True' else 'NO'
#
#         if(len(value) != 0):
#             content = {"networks": newlist}
#         return content, code
#
#         # network_id = ''
#         # if name != '':
#         #     for network in networklist:
#         #         for k, v in network.iteritems():
#         #             if v == name:
#         #                 network_id = network.get('id', '')
#         #                 break
#         #     return network_id
#     except HTTPError:
#         raise 'not found server'


# 15.3.2 create subnet
def create_subnet(**subnet):
    req = urllib2.Request(neutron_url+'/v2.0/subnets')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(subnet))
        code = response.getcode()
        content = json.loads(response.read())

        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# list subnet
def list_subnet():
    req = urllib2.Request(neutron_url+'/v2.0/subnets')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())

        subnetlist = content['subnets']

        syslist = []
        for subnet in subnetlist:
            if(subnet['tenant_id'] == 'd04021d5a4144b4c9f579fdc1d1c2a9a'):
                syslist.append(subnet)

        content = {'subnets': syslist}
        return content, code
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# delete subnet
def delete_subnet():
    req = urllib2.Request(neutron_url+'/v2.0/subnets/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()

        return code
    except HTTPError:
        raise 'not found server'
    except URLError,e:
        raise 'URLError:', e.reason


# 15.2.6 delete network parameter: network name
def delete_network(id):
    req = urllib2.Request(neutron_url+'/v2.0/networks/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        if 204 == code:
            data = {"status": "ok"}
        return data
    except HTTPError:
        raise 'not found server'


# 16.9.8 list floating ip
def list_floatingip(status):
    req = urllib2.Request(neutron_url+'/v2.0/floatingips')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        # print content

        iplist = content['floatingips']
        active_list = []
        down_list = []
        for ip in iplist:
            if(ip['status'] == 'ACTIVE'):
                active_list.append(ip)
            if(ip['status'] == 'DOWN'):
                down_list.append(ip)

        if status == 'ACTIVE':
            content = {'floatingips': active_list}
        if status == 'DOWN':
            content = {'floatingips': down_list}
        # print content
        return content, code
    except HTTPError:
        raise 'not found server'


# 16.9.12 delete floating ip   parameter:floating ip id
def delete_floatingip(id):
    req = urllib2.Request(neutron_url+'/v2.0/floatingips/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()

        return code
    except HTTPError:
        raise 'not found server'


# 16.9.9  create floating ip
def create_floatingip():
    data = {
        "floatingip": {
            "floating_network_id": "8467c174-2e3d-4661-8030-bcff99f749b5"
        }
    }

    req = urllib2.Request(neutron_url+'/v2.0/floatingips')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(data))
        code = response.getcode()
        content = json.loads(response.read())


        return code
    except HTTPError:
        raise 'not found server'


# 12.2.5 associate or disassociate ip to port
def update_floatingip(id, **port):
    if '.' in id:
        ipdic = list_floatingip('ACTIVE')
        iplist = ipdic[0]['floatingips']
        for ip in iplist:
            if ip['floating_ip_address'] == id:
                id = ip['id']
                break
    req = urllib2.Request(neutron_url+'/v2.0/floatingips/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(port))
        code = response.getcode()
        # content = json.loads(response.read())
        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'

# 16.7.1 list security group
def list_securitygroup():
    req = urllib2.Request(neutron_url+'/v2.0/security-groups')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        return content, code
    except HTTPError:
        raise 'not found server'


# 16.7.2 create security group
def create_securitygroup(**group):
    req = urllib2.Request(neutron_url+'/v2.0/security-groups')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(group))
        code = response.getcode()
        content = json.loads(response.read())

        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# 12.2.5 update securitygroup
def update_securitygroup(id, **group):
    req = urllib2.Request(neutron_url+'/v2.0/security-groups/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(group))
        code = response.getcode()
        content = json.loads(response.read())
        # print code, content
        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'

# 16.7.5
def delete_securitygroup(id):

    req = urllib2.Request(neutron_url+'/v2.0/security-groups/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        if 204 == code:
            data = {"status": "ok"}
        return data
    except HTTPError:
        raise 'not found server'


# list security group rules
def list_secgrouprules():
    req = urllib2.Request(neutron_url+'/v2.0/security-group-rules')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        newcontent = content.values()

        return newcontent
    except HTTPError:
        raise 'not found server'


# create ecurity group rules
def create_secgourprules(rule_list):
    req = urllib2.Request(neutron_url+'/v2.0/security-group-rules')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        codes = []
        contents = []
        for rule in rule_list:
            response = urllib2.urlopen(req, json.dumps(rule))
            code = response.getcode()
            content = json.loads(response.read())
            codes.append(code)
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}

    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason




# list projects
def list_project():
    req = urllib2.Request(service_ip+'35357/v3/projects')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        newcontent = content.values()
        # print code
        return newcontent, code
    except HTTPError:
        raise 'not found server'


# list pool
def list_pool():
    req = urllib2.Request(service_ip+'8774/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/os-floating-ip-pools')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        newcontent = content['floating_ip_pools']
        # print 'newcontent', newcontent
        return newcontent, code
    except HTTPError:
        raise 'not found server'


#   allocate ip
def allocate_ip(**ip):
    req = urllib2.Request(service_ip+'8774/v2/d04021d5a4144b4c9f579fdc1d1c2a9a/os-floating-ip-pools')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(ip))
        code = response.getcode()
        content = json.loads(response.read())
        # print code, content
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


def list_routers(user):
    req = urllib2.Request(neutron_url+'/v2.0/routers')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        opcache = []
        params = ''
        opcache = Opcache.objects.filter(user=user).filter(params=params).filter(category='list_routers')
	content = ''
        if opcache is not None and len(opcache) >0:
            code = 200
            content = json.loads(opcache[0].content)
	else:
            response = urllib2.urlopen(req)
            code = response.getcode()
            data = response.read()
            content = json.loads(data)
            if code == 200:
                o = Opcache()
                o.user = user
                o.category = 'list_routers'
                o.params = params
                o.content = data
                o.save()
        return content, code
    except HTTPError:
        raise 'not found server'


def list_routers(tetantid = None):
    req = urllib2.Request(neutron_url+'/v2.0/routers')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        if(tetantid != None):
            newcontent = []
            routerlist = content['routers']
            for router in routerlist:
                if router['tenant_id'] == tetantid:
                    newcontent.append(router)

            content = {'routers': newcontent}
        return content, code
    except HTTPError:
        raise 'not found server'


#add port_list_bynobind to get the port list that not bind to any instance
def list_ports_by_nobind(**network):
    req = urllib2.Request(neutron_url+'/v2.0/ports?network_id='+network.get('network_id'))
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        ports = content['ports']
        port_list = []

        if code == 200 and ports is not None:
            print 'network.get(network_id):----',network.get('network_id')
            for port in ports:

                if port.get('device_id') is None or port.get('device_id') =='':#if not binded then  record
                    port_dict = {}
                    port_dict['id'] = port.get('id')
                    for ip in port.get('fixed_ips'):
                        port_dict['ip_address'] = ip.get('ip_address')
                    port_list.append(port_dict)
        print 'port_list:',port_list
        return port_list
    except HTTPError:
        raise 'not found port'


def list_ports():
    tenantid = 'd04021d5a4144b4c9f579fdc1d1c2a9a'
    req = urllib2.Request(neutron_url+'/v2.0/ports?tenant_id='+tenantid)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        ports = content['ports']
        # json.dump(content, open('list_network.json', 'w'), indent=4)


        portslist = []
        for port in ports:
            if 'compute:' in port['device_owner']:
                deviceid = port['device_id']
                devicename = list_server(tenantid, deviceid)
                newname = devicename + ":" + port['fixed_ips'][0]['ip_address']
                dict = {"id": port['id'], "name": newname}

                portslist.append(dict)

        # print portslist
        newcontent = {'ports': portslist}

        return newcontent, code
    except HTTPError:
        raise 'not found server'


def list_server(tenantid, serviceid):
    req = urllib2.Request(NOVAL_URL+'v2/' + tenantid + '/servers/' + serviceid)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        content = json.loads(response.read())
        servername = content['server']['name']
        return servername
    except HTTPError:
        raise 'not found server'


def create_router(**router):
    req = urllib2.Request(neutron_url+'/v2.0/routers')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(router))
        code = response.getcode()
        content = json.loads(response.read())
        # print code, content
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


def add_interface(routerid, **subnet):
    req = urllib2.Request(neutron_url+'/v2.0/routers/'+routerid+'/add_router_interface')
    # print neutron_url+'/v2.0/routers/'+routerid+'/add_router_interface'
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(subnet))
        code = response.getcode()
        content = json.loads(response.read())

        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "add failed"}
    except HTTPError:
        raise 'not found server'


# 15.2.6 delete router parameter: router id
def delete_router(id):
    req = urllib2.Request(neutron_url+'/v2.0/routers/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        if 204 == code:
            data = {"status": "ok"}
        return data
    except HTTPError:
        raise 'not found server'


# 12.2.5 update router
def update_router(id, **router):
    req = urllib2.Request(neutron_url+'/v2.0/routers/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(router))
        code = response.getcode()
        content = json.loads(response.read())

        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'


# 16.7.1 list  load balancers
def list_lbpools():
    req = urllib2.Request(neutron_url+'/v2.0/lb/pools')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        return content, code
    except HTTPError:
        raise 'not found server'


# 16.7.1 list  loadbalancers
def list_lbmonitors():
    req = urllib2.Request(neutron_url+'/v2.0/lb/health_monitors')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        return content, code
    except HTTPError:
        raise 'not found server'


# create lb member
def create_lbmember(**member):
    req = urllib2.Request(neutron_url+'/v2.0/lb/members')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(member))
        code = response.getcode()
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# create lb pool
def create_lbpool(**pool):
    req = urllib2.Request(neutron_url+'/v2.0/lb/pools')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(pool))
        code = response.getcode()
        content = json.loads(response.read())
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# update lb pool
def update_lbpool(id, **pool):
    req = urllib2.Request(neutron_url+'/v2.0/lb/pools/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(pool))
        code = response.getcode()
        content = json.loads(response.read())
        print code, content
        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'


# 15.2.6 delete firewall parameter: router id
def delete_lbpool(id):
    req = urllib2.Request(neutron_url+'/v2.0/lb/pools/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        if 204 == code:
            data = {"status": "ok"}
        return data
    except HTTPError:
        raise 'not found server'


# associate monitor to pool
def associate_monitor(id, **monitor):
    req = urllib2.Request(neutron_url+'/v2.0/lb/pools/'+id+'/health_monitors')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(monitor))
        code = response.getcode()
        content = json.loads(response.read())
        print code, content
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# 15.2.6 disassociate monitor
def disassociate_monitor(poolid, monitorid):
    req = urllib2.Request(neutron_url+'/v2.0/lb/pools/'+poolid+'/health_monitors/'+monitorid)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        if 204 == code:
            data = {"status": "ok"}
        return data
    except HTTPError:
        raise 'not found server'


# add lb monitor
def add_lbmonitor(**monitor):
    req = urllib2.Request(neutron_url+'/v2.0/lb/health_monitors')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(monitor))
        code = response.getcode()
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# 16.7.1 list  firewall
def list_firewalls():
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewalls')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        return content, code
    except HTTPError:
        raise 'not found server'


# 16.7.1 list  firewall policy
def list_policys():
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewall_policies')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        return content, code
    except HTTPError:
        raise 'not found server'


def create_firewall(**fw):
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewalls')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(fw))
        code = response.getcode()
        # content = json.loads(response.read())
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# 15.2.6 delete firewall parameter: router id
def delete_firewall(id):
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewalls/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'DELETE'
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        if 204 == code:
            data = {"status": "ok"}
        return data
    except HTTPError:
        raise 'not found server'


# firewall policy
def create_fwpolicy(**policy):
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewall_policies')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        # print json.dumps(policy)
        response = urllib2.urlopen(req, json.dumps(policy))
        code = response.getcode()
        # content = json.loads(response.read())
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason

# 16.7.1 list  firewall rules   /v2.0/fw/firewall_rules
def list_fwrules():
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewall_rules')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        content = json.loads(response.read())
        return content, code
    except HTTPError:
        raise 'not found server'


# firewall rule
def create_fwrule(**rule):
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewall_rules')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    try:
        response = urllib2.urlopen(req, json.dumps(rule))
        code = response.getcode()
        # content = json.loads(response.read())
        if code == 201:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError, e:
            if 404 == e.code:
                raise 'not found the server'
    except URLError, e:
            raise 'URLError: ', e.reason


# 12.2.5 update firewall
def update_firewall(id, **fw):
    req = urllib2.Request(neutron_url+'/v2.0/fw/firewalls/'+id)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Auth-Token', gettoken_new())
    req.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(req, json.dumps(fw))
        code = response.getcode()
        content = json.loads(response.read())
        # print code, content
        if code == 200:
            return {"Success": "OK"}
        else:
            return {"Error": "create failed"}
    except HTTPError:
        raise 'not found server'



# create_secgourprules_test()

# user = {'projectid': 'd04021d5a4144b4c9f579fdc1d1c2a9a', 'username': 'admin', 'password':'Abc12345'}
# content = nova_api.list_server_detail(user)
# print content

# list_server('d04021d5a4144b4c9f579fdc1d1c2a9a', '1abbd2eb-c4f2-4992-842c-613ec510e107')
# list_ports()

# list_routers()

# list_pool()

# list_secgrouprules()

# create_network()

# create_subnet('5a9fb3a8-ab4e-44eb-80c5-c7fda17b3a0f')


# list_subnet()

# list_subnet()


# delete_network('tcx')

# list_network()

# create_floatingip()

# delete_floatingip('7b9efbd8-496e-46a1-85e4-a8c04df2b966')

# create_securitygroup()

# delete_securitygroup('153a8423-d27b-44e0-8452-c68f4c6baf22')

# list_securitygroup()

# list_floatingip()

# update_network()
# user={"username":"admin","password":"Abc12345","projectid":"d04021d5a4144b4c9f579fdc1d1c2a9a"}
# network_id={'network_id':'52ea0274-692b-4ef2-a37b-d56fc2561af4'}
# list_ports_by_nobind(**network_id)