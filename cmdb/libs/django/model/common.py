# -*- coding:utf8 -*-
"""
Created on 16/10/1 上午12:06
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.db import models


class CreateUpdateDateTimeCommonModelMixin(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True, help_text='更新时间')

    class Meta:
        abstract = True
