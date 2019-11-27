from django.shortcuts import render
from django.views import generic

class LiveView(generic.TemplateView):
    template_name = "PPLive/liveView.html"

