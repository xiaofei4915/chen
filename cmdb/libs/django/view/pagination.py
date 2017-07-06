# -*- coding:utf8 -*-
"""
Created on 16/10/7 下午11:19
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class OffAblePageNumberPagination(PageNumberPagination):
    """
    可通过?page=off关闭的分页
    """
    page_size = 20
    page_size_query_param = 'page-size'

    def paginate_queryset(self, queryset, request, view=None):

        if 'page' in request.query_params and request.query_params.get('page', '') == 'off':
            return None
        return super(OffAblePageNumberPagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """
        重写该方法, 自定义response数据
            1、获取更全的分页数据, 如总页数等
            2、提供一种再response前, 扩展response数据的方法
        """
        context = OrderedDict([
            ('page_total', self.page.paginator.num_pages),
            ('page_size', self.page_size),
            ('page_number', self.page.number),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(context)
