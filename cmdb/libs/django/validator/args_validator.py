#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年1月30日
    参数验证器
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging

from django.utils.encoding import smart_unicode

log = logging.getLogger(__name__)


def str_arg_validator(arg_name, value, require=True):
    """
    验证简单字符串值的参数
    :param arg_name:
    :return:
    """
    if value is None:
        if require:
            raise ValueError('字符串参数"{name}"是必须需的,但其值为"{value}",参数值错误.'.format(
                name=arg_name, value=smart_unicode(value)))
        return True, '字符串参数"{name}"是可选参数,其值为"{value}".'.format(
            name=arg_name, value=smart_unicode(value))

    if isinstance(value, str) and value:
        if value:
            return True
        else:
            raise ValueError('字符串参数"{name}"的值为空,参数值错误.'.format(name=arg_name))
    else:
        raise TypeError('参数"{name}"必须为字符串类型,但当前其值为"{value_type}".'.format(
            name=arg_name, value_type=type(value)))


def obj_attr_str_validator(obj, arg_name, require=True):
    """
    验证简单字符串值的参数
    :param arg_name:
    :return:
    """
    value = getattr(obj, arg_name)

    if value is None:
        if require:
            raise ValueError('字符串属性"{name}"是对象{obj}必须需的,但其值为"{value}",参数值错误.'.format(
                name=arg_name, obj=smart_unicode(obj), value=smart_unicode(value)))
        return True, '字符串属性"{name}"是对象{obj}可选属性,其值为"{value}".'.format(
            name=arg_name, obj=smart_unicode(obj), value=smart_unicode(value))

    if isinstance(value, str) and value:
        if value:
            return True
        else:
            raise ValueError('对象"{obj}"的字符串属性"{name}"的值为空,参数值错误.'.format(obj=obj, name=arg_name))
    else:
        raise TypeError('对象"{obj}"的属性"{name}"必须为字符串类型,但当前其值为"{value_type}".'.format(
            obj=obj, name=arg_name, value_type=type(value)))


class ArgsValidatorMixin(object):

    @classmethod
    def str_attr_validator(cls, obj, arg_name, require=True):
        return obj_attr_str_validator(obj, arg_name, require)