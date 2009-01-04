#coding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext

from spam.settings import ENCODING

from utils.djangoutils import XMLResponse

class SecurityQuestion(object):

    def __init__(self, question_id, question, anwser):
        self.question_id = question_id
        self.question = question
        self.answer = answer

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
    encoded_email, encoded_domain, encoded_country = encoded_email.split('+')
    decoded_email = "%s@%s.%s" % (encoded_email.decode(ENCODING), encoded_domain.decode(ENCODING), encoded_country.decode(ENCODING))

    question_generator = SecurityQuestionGenerator()

    if request.is_ajax():
        return XMLResponse('mailto_response.xml', {'email' : email, 'i' : int(request.GET['index'])})

    context = {}
    if request.method == 'POST':
        security_question = question_generator.get_security_question(int(request.POST['id']))
        if request.POST['answer'].strip() == security_question.answer:
            #TODO: Senda með öryggisstreng
            return HttpResponseRedirect("%s?email=%s" % (reverse('mailto-safe'), email))
        else:
            return HttpResponseRedirect(request.path)
    else:
        context = {'question' : question_generator.get_random_security_question() }
    return render_to_response('spam/mailto_base.html', context , context_instance = RequestContext(request))

def show_email(request):
    context = {}
    if request.method == 'GET':
        context['email'] = request.GET['email']
        return render_to_response('spam/mailto_base.html', context , context_instance = RequestContext(request))