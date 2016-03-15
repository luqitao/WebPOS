from django.db import transaction

import uuid

from models import *
from rest_framework import serializers


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('id',
                  'company_id',
                  'company_name',
                  'company_address',
                  'company_contact_person',
                  'company_contact_phone')

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.company_address = validated_data.get('company_address', instance.company_address)
        instance.company_contact_person = validated_data.get('company_contact_person', instance.company_contact_person)
        instance.company_contact_phone = validated_data.get('company_contact_phone', instance.company_contact_phone)

        return instance


class ProjectSerializerBase(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('project_openstack_id',
                  'project_openstack_domain_id',
                  'project_openstack_domain_name',
                  'project_name',
                  'project_desc',
                  'project_cpu_quota',
                  'project_mem_quota',
                  'project_store_quota',
                  'project_ip_quota',
                  'project_quota_latest_update',
                  'project_company')


class ProjectSerializerForRelation(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('project_openstack_id',
                  'project_openstack_domain_id',
                  'project_openstack_domain_name',
                  'project_name',
                  'project_desc',
                  'project_cpu_quota',
                  'project_mem_quota',
                  'project_store_quota',
                  'project_ip_quota',
                  'project_quota_latest_update')


class ProjectSerializerReadonly(ProjectSerializerBase):
    project_company = CompanySerializer(many=False, read_only=True)


class ProjectSerializerWritableWithNewCompany(ProjectSerializerBase):
    """Create new project with new company
    """
    project_company = CompanySerializer(many=False)

    def create(self, validated_data):
        with transaction.atomic():
            from appName.api.key_store import create_project as api_create_project
            api_param_user = {u'username': u'admin',
                              u'password': u'Abc12345'}

            api_param_project = {u'project': {u'enable': True,
                                              u'name': validated_data.get('project_name'),
                                              u'description': validated_data.get('project_desc')}}
            code, project_from_openstack = api_create_project(api_param_user, **api_param_project)
            if code == 201:
                company_data = validated_data.pop('project_company')
                validated_data.pop('project_openstack_domain_id')
                validated_data.pop('project_openstack_id')
                company = Company.objects.create(**company_data)
                Project.objects.create(project_company=company,
                                       project_openstack_id=project_from_openstack['project']['id'],
                                       project_openstack_domain_id=project_from_openstack['project']['domain_id'],
                                       **validated_data)
                return Project


class ProjectSerializerWritableWithExistsCompany(ProjectSerializerBase):
    """ Create new project with company with already exists in system
    """
    project = ProjectSerializerBase(many=False)

    def create(self, validated_data):
        project = validated_data.pop('project')
        with transaction.atomic():
            from appName.api.key_store import create_project as api_create_project
            api_param_user = {u'username': u'admin',
                              u'password': u'Abc12345'}

            api_param_project = {u'project': {u'enable': True,
                                              u'name': validated_data.get('project_name'),
                                              u'description': validated_data.get('project_desc')}}
            code, project_from_openstack = api_create_project(api_param_user, **api_param_project)
            if code == 201:
                validated_data.pop('project_openstack_domain_id')
                validated_data.pop('project_openstack_id')
                return Project.objects.create(project_openstack_id=project_from_openstack['project']['id'],
                                              project_openstack_domain_id=
                                              project_from_openstack['project']['domain_id'],
                                              **project)

    def update(self, instance, validated_data):
        with transaction.atomic():
            from appName.api.key_store import update_project_quota \
                as api_update_project_quota
            api_param_user = {u'username': u'admin',
                              u'password': u'Abc12345'}

            api_param_quota = {u'quota_set': {}}

            api_update_project_quota(api_param_user,
                                     instance.project_openstack_id,
                                     instance.project_openstack_id)
            instance.project_desc = validated_data.get('project_desc', instance.project_desc)
            instance.project_cpu_quota = validated_data.get('project_cpu_quota', instance.project_cpu_quota)
            instance.project_mem_quota = validated_data.get('project_mem_quota', instance.project_mem_quota)
            instance.project_store_quota = validated_data.get('project_store_quota', instance.project_store_quota)
            instance.project_ip_quota = validated_data.get('project_ip_quota', instance.project_ip_quota)
            instance.save()
            return instance


class PortalUserSerializerBase(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PortalUser
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_active',
                  'date_joined',
                  'last_login',
                  'roles',
                  'company',
                  'project'
                  )


class PortalUserSerializerReadonly(PortalUserSerializerBase):
    is_active = serializers.BooleanField(read_only=True)
    project = ProjectSerializerForRelation(many=False, read_only=True)
    company = CompanySerializer(many=False, read_only=True)


class PortalUserSerializerWritable(PortalUserSerializerBase):
    project = serializers.CharField(required=True)

    class Meta:
        model = PortalUser
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'roles',
                  'project'
                  )

    def create(self, validated_data):
        project_id = validated_data.get('project', None)
        if project_id is not None:
            project = Project.objects.get(project_openstack_id=project_id)
            if project is not None:
                company_id = project.project_company
                if 'company' in validated_data:
                    validated_data.pop('company')

                if 'is_active' in validated_data:
                    validated_data.pop('is_active')

                validated_data.pop('project')

                user = PortalUser.objects.create(company=company_id,
                                                 project=project,
                                                 is_active=False,
                                                 is_staff=True,
                                                 is_superuser=False,
                                                 **validated_data)
                email_code = uuid.uuid4()
                email = AuthenticateEmail.objects.create(portal_user=user,
                                                         authenticate_email_code=email_code)
                AuthenticateEmailTask.objects.create(authenticate_email=email)
                return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)

        return instance


class AuthenticateEmailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AuthenticateEmail
        fields = ('id',
                  'portal_user_id',
                  'authenticate_email_code',
                  'authenticate_email_date')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AuthenticateEmailTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AuthenticateEmailTask
        fields = ('id',
                  'authenticate_email_id',
                  'status')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class WorkOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ('portal_user',
                  'portal_project',
                  'portal_project_admin',
                  'word_order_subject',
                  'work_order_status',
                  'create_date',
                  'latest_modify_date')


class WorkOrderDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkOrderDetail
        fields = ('work_order',
                  'work_order_index',
                  'create_date',
                  'work_order_type')


class ResourceOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResourceOrder
        fields = ('order_from',
                  'order_to',
                  'order_project',
                  'resource_order_apply_date',
                  'resource_order_latest_update_date',
                  'resource_status')


class ResourceOrderDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResourceOrderDetail
        fields = ('resource_order',
                  'resource_type',
                  'resource_quantity',
                  'resource_unit',
                  'resource_order_apply_date',
                  'resource_order_latest_update_date',
                  'resource_order_detail_status')
