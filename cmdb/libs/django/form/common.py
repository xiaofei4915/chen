# -*- coding:utf8 -*-
"""
Created on 16/10/1 下午2:57
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from .bootstrap import BootstrapFormStyles
from django import forms


class CommonFormMixin(object):

    def get_form_name(self):
        return self.__class__.__name__


class BootstrapModelForm(BootstrapFormStyles, CommonFormMixin, forms.ModelForm):
    pass


class BootstrapForm(BootstrapFormStyles, CommonFormMixin, forms.Form):
    pass

