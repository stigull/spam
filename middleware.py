#coding: utf-8
import re
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings

from spam.settings import ENCODING

SAFE_URLS = getattr(settings, "SAFE_URLS", [])

MAILTO_REGEX = re.compile(r'\"mailto:(?P<email>[A-Za-z0-9._%-]+)@(?P<domain>[A-Za-z0-9._%-]+)\.(?P<country>[A-Za-z]{2,4})[^"]*\"')
EMAIL_IN_BODY_REGEX = re.compile(r'(?P<email>[A-Za-z0-9._%-]+)@(?P<domain>[A-Za-z0-9._%-]+)\.(?P<country>[A-Za-z]{2,4})')

class ObfuscateEmails(object):

    def process_response(self, request, response):
        try:
            url = reverse('spam-mailto-safe')
        except NoReverseMatch, e:
            #TODO: Notify that spam protection is offline
            return response
        else:
            should_be_bypassed = False
            for safe_url in SAFE_URLS:
                if request.path.startswith(safe_url):
                    should_be_bypassed = True
                    break

            is_mailto_safe = should_be_bypassed or request.path.startswith(url)

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
    return "%s &#091;hjá/at&#093; %s &#091;punktur/dot&#093; %s" % (match.group('email'), match.group('domain'), match.group('country'))

