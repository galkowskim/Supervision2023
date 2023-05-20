from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.http import HttpResponse
from .models import JobAdvertisement

from typing import Any, Optional
import pandas as pd
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from .utils import show_wordcloud


class MainPageJobAdvertisementList(LoginRequiredMixin, ListView):
    model = JobAdvertisement
    context_object_name = 'advertisements'
    template_name = 'job_analyzer/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_advertisements'] = JobAdvertisement.objects.order_by(
            'priority_level')

        date_added_from = self.request.GET.get('date_added_from')
        date_added_to = self.request.GET.get('date_added_to')
        priority_level = self.request.GET.get('priority_level')

        job_advertisements = JobAdvertisement.objects.all()

        if date_added_from and date_added_to:
            date_added_from = datetime.strptime(date_added_from, "%Y-%m-%d")
            date_added_to = datetime.strptime(date_added_to, "%Y-%m-%d")
            job_advertisements = job_advertisements.filter(
                date_added__range=(date_added_from, date_added_to))

        if priority_level:
            job_advertisements = job_advertisements.filter(
                priority_level=priority_level)

        context['job_advertisements'] = job_advertisements

        return context


def details(request, pk):
    job = JobAdvertisement.objects.get(id=pk)
    data = getattr(job, 'content')
    wordcloud = show_wordcloud(data)
    context = {'job': job,
               'wordcloud': wordcloud}
    return render(request, 'job_analyzer/advertisement.html', context)