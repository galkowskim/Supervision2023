from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .models import JobAdvertisement


class MainPageToDoList(LoginRequiredMixin, ListView):
    model = JobAdvertisement
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_advertisements'] = JobAdvertisement.objects.filter(
            user=self.request.user, project=None).order_by('priority_level')
        context['count'] = context['job_advertisements'].filter(
            status_of_completion=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)

        context['search_input'] = search_input
        return context
