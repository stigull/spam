#coding: utf-8
from django.conf.urls.defaults import *

from spam.views import decode_email

urlpatterns = patterns('',
    url(r'^tu-ert-mennskur/', show_email, name='spam-mailto-safe'),
    url(r'^tolvupostfang/$', decode_email),
    url(r'^tolvupostfang/(?P<encoded_email>[A-Za-z0-9._%-]+\+[A-Za-z0-9._%-]+\+[A-Za-z]{2,4})/$', decode_email,
                    name='spam-decode-email'),
)