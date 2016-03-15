from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from views import *

route = routers.SimpleRouter(trailing_slash=False)
route.register(r'company', CompanyViewSet, base_name='company')
route.register(r'project', ProjectViewSet, base_name='project')
route.register(r'portalusers', PortalUserViewSet, base_name='portalusers')
route.register(r'workorder', WorkOrderViewSet, base_name='workorder')
route.register(r'workorderDetail', WorkOrderDetailViewSet, base_name='workorder_detail')
route.register(r'resourceorder', ResourceOrder, base_name='resourceorder')
route.register(r'resourceorderDetail', ResourceOrderDetail, base_name='resourceorder_detail')

urlpatterns = route.urls

urlpatterns += [url(r'^image/', ImageView.as_view(), name='image'),
                url(r'^', PortalView.as_view(), name='main')]
