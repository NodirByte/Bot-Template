from django.shortcuts import render
from .models import Container, User
from django.core.paginator import Paginator
from .services import get_review_statistics_by_container
from django.contrib.auth.mixins import AccessMixin
from django.views.generic import ListView, DetailView



class SuperuserRequiredMixin(AccessMixin):
    """Ensure that the current user is authenticated and is a superuser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    

class IndexView(SuperuserRequiredMixin, ListView):
    model = Container
    template_name = 'containers.html'
    context_object_name = 'containers'
    paginate_by = 10

    def get_queryset(self):
        return Container.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class ContainerDetailView(SuperuserRequiredMixin, DetailView):
    model = Container
    template_name = 'container_detail.html'
    context_object_name = 'container'

    def get_queryset(self):
        return Container.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_statistics'] = get_review_statistics_by_container(self.kwargs['pk'])
        return context
    