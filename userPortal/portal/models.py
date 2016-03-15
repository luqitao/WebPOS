# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class PortalUser(AbstractUser):
    """User data model
    extends django default user data
    """

    ROLE_SUPER_ADMIN = 'AD'
    ROLE_SYSTEM_ADMIN = 'SA'
    ROLE_PROJECT_ADMIN = 'PA'
    ROLE_PROJECT_USER = 'PU'

    ROLE_CHOICE = {
        (ROLE_SUPER_ADMIN, u'超级管理员'),
        (ROLE_SYSTEM_ADMIN, u'系统管理员'),
        (ROLE_PROJECT_ADMIN, u'租户管理员'),
        (ROLE_PROJECT_USER, u'用户')
    }

    authenticated = models.BooleanField(default=False)  # Whether authenticated by email
    project = models.ForeignKey('Project',
                                to_field='project_openstack_id',
                                related_name='portal_user_project',
                                null=True)  # project belong to
    company = models.ForeignKey('Company',
                                to_field='company_id',
                                related_name='portal_user_company',
                                null=True)  # company belong to
    roles = models.CharField(max_length=2, choices=ROLE_CHOICE, default=ROLE_SUPER_ADMIN)  # user's role


class Project(models.Model):
    """Project data model
    """

    project_openstack_id = models.CharField(max_length=64, blank=True, unique=True)  # project id from openstack
    project_openstack_domain_id = models.CharField(max_length=254)  # project domain id from openstack
    project_openstack_domain_name = models.CharField(max_length=254)  # project domain name from openstack
    project_name = models.CharField(max_length=254, blank=True)  # project name defined via portal
    project_desc = models.CharField(max_length=254, blank=True)  # project description via portal
    project_company = models.ForeignKey('Company',
                                        to_field='company_id',
                                        related_name='project_company')  # company belong to
    project_cpu_quota = models.IntegerField(blank=True)  # cpu quality quota defined by administrator
    project_mem_quota = models.IntegerField(blank=True)  # ram capacity quota defined by administrator
    project_store_quota = models.IntegerField(blank=True)  # store capacity quota defined by administrator
    project_ip_quota = models.IntegerField(blank=True)  # ip quality quota defined by administrator
    project_quota_latest_update = models.DateTimeField(blank=True)  # latest quota modification time


class ProjectAdmin(models.Model):
    """Project's Admin
    """
    project = models.OneToOneField('Project', to_field='project_openstack_id', related_name='project_admin_project')
    portal_user = models.ForeignKey('PortalUser', related_name='project_admin_user')


class Company(models.Model):
    """Company data model
    """

    company_id = models.CharField(max_length=64, blank=True, unique=True)  # company identify
    company_name = models.CharField(max_length=64, blank=True, unique=True)  # company name defined in users profile
    company_address = models.CharField(max_length=254)  # company contact address defined in users profile
    company_contact_person = models.CharField(max_length=254)  # company contact person defined in user profile
    company_contact_phone = models.CharField(max_length=254)  # company contact phone defined in user profile


class AuthenticateEmail(models.Model):
    """Register authenticate email data model
    """

    authenticate_email_code = models.CharField(max_length=64, unique=True)  # verification code in authentication email
    authenticate_email_date = models.DateTimeField(auto_now=True)  # when verification code generated
    portal_user = models.ForeignKey('PortalUser', related_name='email_user')  # portal user


class AuthenticateEmailTask(models.Model):
    """Authentication Email Automatic Sending Task
    """

    EMAIL_STATUS_WAIT = 0
    EMAIL_STATUS_SEND = 1

    EMAIL_STATUS_CHOICE = {
        (EMAIL_STATUS_WAIT, u'等待发送'),
        (EMAIL_STATUS_SEND, u'已发送'),
    }

    authenticate_email = models.ForeignKey('AuthenticateEmail', related_name='task_email')
    status = models.IntegerField(blank=True,
                                 choices=EMAIL_STATUS_CHOICE,
                                 default=EMAIL_STATUS_WAIT)


class ResourceOrder(models.Model):
    """Resource order Master record
    """

    RESOURCE_ORDER_STATUS_PENDING = 0  # status waiting for handle
    RESOURCE_ORDER_STATUS_REJECT = 1  # status reject by admin
    RESOURCE_ORDER_STATUS_ACCEPTED_PREPARING = 2  # status order accepted but still in preparing
    RESOURCE_ORDER_STATUS_ACCEPTED_ACCOMPLISHED = 3  # status accomplished

    RESOURCE_ORDER_STATUS_CHOICE = {
        (RESOURCE_ORDER_STATUS_PENDING, u'等待处理'),
        (RESOURCE_ORDER_STATUS_REJECT, u'拒绝'),
        (RESOURCE_ORDER_STATUS_ACCEPTED_PREPARING, u'创建中'),
        (RESOURCE_ORDER_STATUS_ACCEPTED_ACCOMPLISHED, u'创建完成')
    }

    portal_user = models.ForeignKey('PortalUser', related_name='order_from')  # user from
    portal_project = models.ForeignKey('Project', related_name='order_project')  # project within
    portal_project_admin = models.ForeignKey('PortalUser', related_name='order_to')  # project administrator send to
    resource_order_apply_date = models.DateTimeField(auto_now=True)
    resource_order_latest_update_date = models.DateTimeField(blank=True)
    resource_status = models.IntegerField(blank=True,
                                          choices=RESOURCE_ORDER_STATUS_CHOICE,
                                          default=RESOURCE_ORDER_STATUS_PENDING)


class ResourceOrderDetail(models.Model):
    """Resource order detail records
    """

    RESOURCE_ORDER_STATUS_PENDING = 0  # status waiting for handle
    RESOURCE_ORDER_STATUS_REJECT = 1  # status reject by admin
    RESOURCE_ORDER_STATUS_ACCEPTED_PREPARING = 2  # status order accepted but still in preparing
    RESOURCE_ORDER_STATUS_ACCEPTED_ACCOMPLISHED = 3  # status accomplished

    RESOURCE_ORDER_STATUS_CHOICE = {
        (RESOURCE_ORDER_STATUS_PENDING, u'等待处理'),
        (RESOURCE_ORDER_STATUS_REJECT, u'拒绝'),
        (RESOURCE_ORDER_STATUS_ACCEPTED_PREPARING, u'创建中'),
        (RESOURCE_ORDER_STATUS_ACCEPTED_ACCOMPLISHED, u'创建完成')
    }

    resource_order = models.ForeignKey('ResourceOrder')
    resource_type = models.IntegerField()
    resource_quantity = models.IntegerField(blank=True)
    resource_unit = models.CharField(blank=True, max_length=254)
    resource_order_apply_date = models.DateTimeField(blank=True, auto_now=True)
    resource_order_latest_update_date = models.DateTimeField(blank=True)
    resource_order_detail_status = models.IntegerField(blank=True,
                                                       choices=RESOURCE_ORDER_STATUS_CHOICE,
                                                       default=RESOURCE_ORDER_STATUS_PENDING)


class WorkOrder(models.Model):
    """Work order master record
    """

    WORK_ORDER_STATUS_PROCESS = 0
    WORK_ORDER_STATUS_ACCOMPLISH = 1

    WORK_ORDER_STATUS_CHOICE = {
        (WORK_ORDER_STATUS_PROCESS, u'处理中'),
        (WORK_ORDER_STATUS_ACCOMPLISH, u'处理完成'),
    }

    portal_user = models.ForeignKey('PortalUser', related_name='portal_user_work_order_from')
    portal_project = models.ForeignKey('Project')
    portal_project_admin = models.ForeignKey('PortalUser', related_name='portal_user_work_order_to')

    word_order_subject = models.CharField(blank=True, max_length=254)

    work_order_status = models.IntegerField(blank=True,
                                            choices=WORK_ORDER_STATUS_CHOICE,
                                            default=WORK_ORDER_STATUS_PROCESS)

    create_date = models.DateTimeField(blank=True, auto_now=True)
    latest_modify_date = models.DateTimeField(blank=True, auto_now=True)


class WorkOrderDetail(models.Model):
    """Work order detail records
    """

    WORK_ORDER_TYPE_SEND = 0
    WORK_ORDER_TYPE_REPLY = 1

    WORK_ORDER_TYPE_CHOICE = {
        (WORK_ORDER_TYPE_SEND, '发起'),
        (WORK_ORDER_TYPE_REPLY, '回复'),
    }

    work_order = models.ForeignKey('WorkOrder')
    work_order_index = models.IntegerField(blank=True)
    create_date = models.DateTimeField(blank=True, auto_now=True)

    work_order_type = models.IntegerField(blank=True,
                                          choices=WORK_ORDER_TYPE_CHOICE,
                                          default=WORK_ORDER_TYPE_SEND)
