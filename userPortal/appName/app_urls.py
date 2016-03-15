"""myServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, url
from appName import views

urlpatterns = patterns("",
    url(r'^$', views.open_index),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^index/$', views.open_index),
    url(r'^test/$', views.open_index),
    url(r'^listTest/$', views.open_index),

    # cinder
    url(r'^volumes/$', views.open_index),
    url(r'^volumeinfo/$', views.volumeinfo),
    url(r'^volumes/\?tab=volumes_tab$', views.volumeinfo, name='volumes_tab'),
    url(r'^volumes/\?tab=snapshots_tab$', views.open_index, name='snapshots_tab'),
    url(r'^createVolume/$', views.create_volume),
    url(r'^updateVolume/$', views.update_volume),
    url(r'^deleteVolume/$', views.delete_volume),
    url(r'^attachVolume/$', views.attach_volume),
    url(r'^detachVolume/$', views.detach_volume),
    url(r'^createSnapshot/$', views.create_snapshot),
    url(r'^snapshotinfo/$', views.snapshotinfo),
    url(r'^updateSnapshot/$', views.update_snapshot),
    url(r'^deleteSnapshot/$', views.delete_snapshot),


    #images added by aaron begin
    url(r'^glance/$', views.open_index),
    url(r'^listGlance/$', views.open_glance),
    url(r'^deleteImage/*', views.delete_image),
    url(r'^createImage/', views.create_image),
    url(r'^editImage/', views.update_image),
    #images added by aaron end

    #instances added by aaron begin
    url(r'^instance/$', views.open_index),
    url(r'^listInstance/$', views.open_instance),
    url(r'^list_flavor/$', views.list_flavor),
    url(r'^launchInstance/*', views.launch_instance),
    url(r'^terminateInstance/', views.terminate_instance),
    url(r'^operateInstance/', views.operate_instance),
    url(r'^pauseInstance/', views.pause_instance),
    url(r'^instance/list_network_names/', views.list_network_names),
    url(r'^instance/list_network_port_names/', views.list_network_port_names),
    url(r'^instance/list_imageNames/', views.list_image_names),
    url(r'^instance/console_url/', views.get_console_url),
    #instances added by aaron end


     #images added by aaron begin
    url(r'^user/$', views.open_index),
    url(r'^listUser/$', views.get_user),
    url(r'^deleteUser/*', views.delete_user),
    url(r'^createUser/', views.create_user),
    url(r'^listUserRole/', views.list_user_role),
    url(r'^listProjectName/', views.list_project_name),
    url(r'^editUser/', views.update_user),
    #images added by aaron end

    #project added by aaron begin
    url(r'^project/$', views.open_index),
    url(r'^listProject/$', views.list_project),
    url(r'^listUserName/$', views.list_all_user_names),
    url(r'^deleteProject/*', views.delete_project),
    url(r'^createProject/', views.create_project),
    url(r'^editProject/', views.update_project),
    #project added by aaron end

    # ceilometer
    url(r'^ceilometer/$', views.open_index),
    url(r'^get_ceilometer/list_meters/', views.ceilometers_get_meters),
    url(r'^get_ceilometer/list_alarms/', views.ceilometers_get_alarms),
    url(r'^get_ceilometer/total/$', views.ceilometer_total),
    url(r'^get_ceilometer/information/', views.getInformation),

    # neutron
    url(r'^neutron/$', views.open_index),
    url(r'^neutron/list_networks/$', views.neutron_info.list_networks),
    url(r'^neutron/delete_networks/*', views.neutron_info.delete_networks),
    url(r'^neutron/create_network/', views.neutron_info.create_network),
    url(r'^neutron/update_network/', views.neutron_info.update_network),
    url(r'^neutron/list_project/', views.neutron_info.list_projects),
    url(r'^neutron/create_subnet/', views.neutron_info.create_subnet),
    url(r'^neutron/list_subnet/', views.neutron_info.list_subnets),


    url(r'^floatingip/$', views.open_index),
    url(r'^floatingip/list_floatingip/$', views.neutron_info.list_floatingip),
    url(r'^floatingip/allocate_floatingip/', views.neutron_info.allocate_floatingip),
    url(r'^floatingip/list_pool/', views.neutron_info.list_pool),
    url(r'^floatingip/list_ports/', views.neutron_info.list_ports),
    url(r'^floatingip/associate_ip/', views.neutron_info.associate_ip),
    url(r'^floatingip/disassociate_ip/', views.neutron_info.disassociate_ip),

    url(r'^router/$', views.open_index),
    url(r'^router/list_routers/', views.neutron_info.list_routers),
    url(r'^router/list_extnet/', views.neutron_info.list_extnet),
    url(r'^router/create_router/', views.neutron_info.create_router),
    url(r'^router/add_interface/', views.neutron_info.add_interface),
    url(r'^router/delete_router/', views.neutron_info.delete_router),
    url(r'^router/update_router/', views.neutron_info.update_router),

    url(r'^securitygroup/$', views.open_index),
    url(r'^securitygroup/list_groups/', views.neutron_info.list_groups),
    url(r'^securitygroup/create_group/', views.neutron_info.create_group),
    url(r'^securitygroup/delete_group/', views.neutron_info.delete_group),
    url(r'^securitygroup/update_group/', views.neutron_info.update_group),
    url(r'^securitygroup/add_grouprules/', views.neutron_info.add_grouprules),


    url(r'^loadbalancer/$', views.open_index),
    url(r'^loadbalancer/list_pools/', views.neutron_info.list_lbpools),
    url(r'^loadbalancer/add_lbpool/', views.neutron_info.add_lbpool),
    url(r'^loadbalancer/delete_lbpool/', views.neutron_info.delete_lbpool),
    url(r'^loadbalancer/list_monitor/', views.neutron_info.list_monitors),
    url(r'^loadbalancer/associate_monitor/', views.neutron_info.associate_monitor),
    url(r'^loadbalancer/disassociate_monitor/', views.neutron_info.disassociate_monitor),
    url(r'^loadbalancer/add_monitor/', views.neutron_info.add_lbmonitor),
    url(r'^loadbalancer/edit_lbpool/', views.neutron_info.update_lbpool),
    url(r'^loadbalancer/add_member/', views.neutron_info.add_lbmember),

    url(r'^firewall/$', views.open_index),
    url(r'^firewall/list_firewall/', views.neutron_info.list_firewall),
    url(r'^firewall/update_firewall/', views.neutron_info.update_firewall),
    url(r'^firewall/list_policy/', views.neutron_info.list_policy),
    url(r'^firewall/add_policy/', views.neutron_info.add_policy),
    url(r'^firewall/create_firewall/', views.neutron_info.create_firewall),
    url(r'^firewall/delete_firewall/', views.neutron_info.delete_firewall),
    url(r'^firewall/list_rule/', views.neutron_info.list_fwrule),
    url(r'^firewall/add_fwrule/', views.neutron_info.add_fwrule),
    url(r'^firewall/add_router_to_fw/', views.neutron_info.add_router_to_fw),
    url(r'^firewall/remove_router_to_fw/', views.neutron_info.remove_router_to_fw),




)

