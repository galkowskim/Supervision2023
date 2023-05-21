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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        context['jobs_very_low'] = job_advertisements.filter(priority_level=1).count()
        context['jobs_low'] = job_advertisements.filter(priority_level=2).count()
        context['jobs_medium'] = job_advertisements.filter(priority_level=3).count()
        context['jobs_high'] = job_advertisements.filter(priority_level=4).count()
        context['jobs_very_high'] = job_advertisements.filter(priority_level=5).count()

        return context


def details(request, pk):
    job = JobAdvertisement.objects.get(id=pk)
    data = getattr(job, 'content')
    wordcloud = show_wordcloud(data)
    context = {'job': job,
               'wordcloud': wordcloud}
    return render(request, 'job_analyzer/advertisement.html', context)


@csrf_exempt
def update_fake_status(request: HttpRequest):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_id = request.POST.get('job_id')
        is_fake_str = request.POST.get('is_fake')

        # Convert is_fake_str to a boolean value
        print(is_fake_str)
        print(is_fake_str.lower())
        print(is_fake_str.lower() == 'false')
        if is_fake_str.lower() == 'false':
            new_is_fake = True
            print('here')
        elif is_fake_str.lower() == 'true':
            new_is_fake = False
            print('here2')
        # Retrieve the job advertisement
        try:
            job = JobAdvertisement.objects.get(id=job_id)
        except JobAdvertisement.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Job advertisement not found'})

        # Update the fake status
        job.is_fake = new_is_fake
        print('przed savem: ', new_is_fake)
        print(JobAdvertisement.objects.get(id=job_id).is_fake)
        job.save()
        print('po')
        print(JobAdvertisement.objects.get(id=job_id).is_fake)
        print('\n\n')

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def dashboard(request):
    jobs = JobAdvertisement.objects.all()
    context = {'n_jobs': len(jobs)}
    return render(request, 'job_analyzer/dashboard.html', context)