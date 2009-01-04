#coding: utf-8
import re
from django.core.urlresolvers import reverse

from spam.settings import ENCODING

MAILTO_REGEX = re.compile(r'\"mailto:(?P<email>[A-Za-z0-9._%-]+)@(?P<domain>[A-Za-z0-9._%-]+)\.(?P<country>[A-Za-z]{2,4})[^"]*\"')
EMAIL_IN_BODY_REGEX = re.compile(r'(?P<email>[A-Za-z0-9._%-]+)@(?P<domain>[A-Za-z0-9._%-]+)\.(?P<country>[A-Za-z]{2,4})')

class ObfuscateEmails(object):

    def process_response(self, request, response):
        is_mailto_safe = request.path.startswith(reverse('spam-mailto-safe'))

        if not is_mailto_safe and 'text/html' in response['Content-Type']:
            response.content = MAILTO_REGEX.sub(encode_mail_to, response.content)
            response.content = EMAIL_IN_BODY_REGEX.sub(encode_email_in_body, response.content)
        return response

def encode_mail_to(match):
    email = match.group('email')
    domain = match.group('domain')
    country = match.group('country')
    encoded_email = "%s+%s+%s" % ( email.encode(ENCODING), domain.encode(ENCODING), country.encode(ENCODING) )
    newpath = reverse('spam-decode-email', kwargs = {'encoded_email': encoded_email })
    return '"%s" rel="nofollow" class="mailto"' % newpath

def encode_email_in_body(match):
    return "%s &#091;hjá&#093; %s &#091;punktur&#093; %s" % (match.group('email'), match.group('domain'), match.group('country'))

