# -*- coding:utf8 -*-
"""
Created on 2017/6/27 下午8:59
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

# 导入通用设置
from .common import *


# 导入环境特定配置
try:
    from cmdb.settings.logging import *
except ImportError:
    pass
