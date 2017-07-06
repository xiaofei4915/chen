# -*- coding:utf8 -*-
"""
Created on 16/10/10 下午12:10
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework.relations import PrimaryKeyRelatedField
from collections import OrderedDict


class FullObjectPrimaryKeyRelatedField(PrimaryKeyRelatedField):

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        value_dict = OrderedDict()
        {value_dict.update({key.name: value.__getattribute__(key.name)}) for key in value._meta.fields}
        if hasattr(value._meta.model, 'get_absolute_url'):
            value_dict['__url__'] = value.get_absolute_url()

        return value_dict
