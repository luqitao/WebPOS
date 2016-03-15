import django_filters

from django.db.models import Q
from models import *


class CompanyFilterSet(django_filters.FilterSet):
    """
    Company list query filter:
    """
    company_name = django_filters.CharFilter(name='company_name', lookup_type='contains')
    company_contact_person = django_filters.CharFilter(name='company_contact_person', lookup_type='contains')
    company_contact_phone = django_filters.CharFilter(name='company_contact_phone', lookup_type='contains')
    company_address = django_filters.CharFilter(name='company_address', lookup_type='contains')

    class Meta:
        model = Company
        fields = ['company_name', 'company_contact_person', 'company_contact_phone', 'company_address']


class ProjectFilterSet(django_filters.FilterSet):
    project_openstack_id = django_filters.CharFilter(name='project_openstack_id')
    project_openstack_domain_id = django_filters.CharFilter(name='project_openstack_domain_id')
    project_openstack_domain_name = django_filters.CharFilter(name='project_openstack_domain_name',
                                                              lookup_type='contains')
    project_name = django_filters.CharFilter(name='project_name', lookup_type='contains')
    project_quota_latest_update = django_filters.DateFromToRangeFilter(name='project_quota_latest_update')
    company_name = django_filters.CharFilter(name='project_company__company_name', lookup_type='contains')
    company_id = django_filters.CharFilter(name='project_company__company_id')
    min_cpu_quota = django_filters.NumberFilter(name='project_cpu_quota', lookup_type='gte')
    max_cpu_quota = django_filters.NumberFilter(name='project_cpu_quota', lookup_type='lte')
    cpu_quota = django_filters.NumberFilter(name='project_cpu_quota')
    min_mem_quota = django_filters.NumberFilter(name='project_mem_quota', lookup_type='gte')
    max_mem_quota = django_filters.NumberFilter(name='project_mem_quota', lookup_type='lte')
    mem_quota = django_filters.NumberFilter(name='project_mem_quota')
    min_store_quota = django_filters.NumberFilter(name='project_store_quota', lookup_type='gte')
    max_store_quota = django_filters.NumberFilter(name='project_store_quota', lookup_type='lte')
    store_quota = django_filters.NumberFilter(name='project_store_quota')
    min_ip_quota = django_filters.NumberFilter(name='project_ip_quota', lookup_type='gte')
    max_ip_quota = django_filters.NumberFilter(name='project_ip_quota', lookup_type='lte')
    ip_quota = django_filters.NumberFilter(name='project_ip_quota')

    class Meta:
        model = Project
        fields = ['project_openstack_id',
                  'project_openstack_domain_id',
                  'project_openstack_domain_name',
                  'project_name',
                  'project_quota_latest_update',
                  'company_name',
                  'company_id',
                  'min_cpu_quota',
                  'max_cpu_quota',
                  'cpu_quota',
                  'min_mem_quota',
                  'max_mem_quota',
                  'mem_quota',
                  'min_store_quota',
                  'max_store_quota',
                  'store_quota',
                  'min_ip_quota',
                  'max_ip_quota',
                  'ip_quota'
                  ]


class PortalUserFilter(django_filters.FilterSet):

    username = django_filters.MethodFilter(action='username_filter_method')
    email = django_filters.CharFilter(name='email')
    roles = django_filters.CharFilter(name='roles')
    date_joined = django_filters.DateFromToRangeFilter(name='date_joined')
    last_login = django_filters.DateFromToRangeFilter(name='last_login')
    company = django_filters.CharFilter(name='company__company_id')
    company_name = django_filters.CharFilter(name='company__company_name', lookup_type='icontains')
    project = django_filters.CharFilter(name='project__project_openstack_id')
    project_name = django_filters.CharFilter(name='project__project_name', lookup_type='icontains')
    project_domain = django_filters.CharFilter(name='project__project_openstack_domain_id')
    project_domain_name = django_filters.CharFilter(name='project__project_openstack_domain_name',
                                                    lookup_type='icontaiins')

    class Meta:
        model = PortalUser
        fields = ('username',
                  'email',
                  'roles',
                  'date_joined',
                  'last_login',
                  'company',
                  'company_name',
                  'project',
                  'project_name',
                  'project_domain',
                  'project_domain_name'
                  )

    def username_filter_method(self, queryset, value):
        return queryset.filter(Q(username__icontains=value) |
                               Q(first_name__icontains=value) |
                               Q(last_name__icontains=value))
