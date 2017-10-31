# coding=utf8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def total_view(req):
    context = dict()
    context['hello'] = 'Hello World!'
    return render(req, 'index.html', context)
