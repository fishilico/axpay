# -*- coding: utf-8 -*-
# Copyright (c) 2013 Polytechnique.org. All rights reserved.

from django.conf import settings
from django.views import generic as django_generic_views

from . import generic


class IndexView(generic.TemplateView):
    topnav = 'home'
    template_name = 'index.html'


# Don't use generic.TemplateView, as that would trigger a login redirect loop.
class LoginView(django_generic_views.TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        ctxt = super(LoginView, self).get_context_data(**kwargs)
        next_url = ctxt.get('next') or self.request.GET.get('next') or settings.LOGIN_REDIRECT_URL
        ctxt.update({
            'next': next_url,
            'topnav': '',
            'sidenav': '',
        })
        return ctxt
