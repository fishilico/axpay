# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.


from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.ContributionsIndexView.as_view(), name='index'),
    url(r'^contributors/$', views.ContributorsListView.as_view(), name='contributors'),
    url(r'^contributor/(?P<pk>\d+)/$', views.ContributorDetailView.as_view(), name='contributor-detail'),
    url(r'^export/$', views.ExportView.as_view(), name='exports'),
)
