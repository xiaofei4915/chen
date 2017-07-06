# -*- coding:utf8 -*-
"""
Created on 2017/6/27 下午9:00
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

import os.path
from . import BASE_DIR

BASE_LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    #日志格式
    'formatters': {
        'detailed': {
            'format': '%(levelname)-8s %(asctime)s %(name)-20s[line %(lineno)-4d] %(processName)-10s %(threadName)-10s \
            %(remoteip)-12s %(user)-20s %(message)s'
        },
        'access_log': {
            'format': '%(asctime)s %(remoteip)-12s %(user)-20s %(path)'
        },
    },
    #过滤器
    'filters': {

    },
    #处理器
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        },
        'error_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'cmdb-error.log'),
            'maxBytes': 102400,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'detailed'
        },
        'access_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'cmdb-access.log'),
            'maxBytes': 102400,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'access_log'
        }
    },
    #记录器
    'loggers': {
        '': {
            'handlers': ['console', 'error_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'error_log_file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console', 'access_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}