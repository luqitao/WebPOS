# -*- coding: utf-8 -*-

'''
Override configurations. Such as Product Env should change the below env value
'''

__author__ = 'aaron'

configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'aaron',
        'password': 'aaron',
        'database': 'testing'
    },

     'key_store': 'http://10.89.151.12:35357/',

     'nova': 'http://10.89.151.12:8774/',

     'glance': 'http://10.89.151.12:9292/',

     'neutron': 'http://10.89.151.12:9696',

     'time_out': 30
}
