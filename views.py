#coding: utf-8
from urllib import urlencode

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from spam.settings import ENCODING

from utils.djangoutils import XMLResponse

class SecurityQuestion(object):

    def __init__(self, question_id, question, answer):
        self.question_id = question_id
        self.question = question
        self.answer = answer

    def is_correct_answer(self, answer):
        return self.answer.lower().strip() == answer.lower().strip()

    def get_id(self):
        return self.question_id

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.__unicode__()

class SecurityQuestionGenerator(object):
    def get_security_question(self, id):
        return SecurityQuestion(0, u"Ertu mennskur?", u"Já")

    def get_random_security_question(self):
        return SecurityQuestion(0, u"Ertu mennskur?", u"Já")


def decode_email(request, encoded_email):
    context = {}
    question_generator = SecurityQuestionGenerator()
    if request.method == 'POST':
        security_question = question_generator.get_security_question(int(request.POST['id']))
        if security_question.is_correct_answer(request.POST['answer']):
            #TODO: Senda með öryggisstreng
            encoded_email, encoded_domain, encoded_country = encoded_email.split("+")
            parameters = {'encoded_email': encoded_email, 'encoded_domain': encoded_domain, 'encoded_country': encoded_country }
            url = "%s?%s" % (reverse('spam-mailto-safe'), urlencode(parameters))
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {'question' : question_generator.get_random_security_question() }
    return render_to_response('spam/mailto_base.html', context , context_instance = RequestContext(request))

def show_email(request):
    context = {}
    if request.method == 'GET':
        try:
            encoded_email = request.GET['encoded_email']
            encoded_domain = request.GET['encoded_domain']
            encoded_country = request.GET['encoded_country']
        except KeyError:
            return HttpResponseRedirect(reverse('index'))
        else:
            decoded_email = "%s@%s.%s" % (encoded_email.decode(ENCODING), encoded_domain.decode(ENCODING),
                                                encoded_country.decode(ENCODING))

            context['email'] = decoded_email
            return render_to_response('spam/mailto_base.html', context , context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('index'))