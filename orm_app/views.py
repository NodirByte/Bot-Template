from django.shortcuts import render
from .models import Container, User
from django.core.paginator import Paginator
from .services import get_review_statistics_by_container
from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    container_list = Container.objects.all()
    paginator = Paginator(container_list, 10)  # Show 10 containers per page

    page_number = request.GET.get('page')
    containers = paginator.get_page(page_number)

    return render(request, 'containers.html', {'containers': containers})


def container_detail(request, container_id):
    container = Container.objects.get(pk=container_id)
    review_statistics = get_review_statistics_by_container(container_id)
    return render(request, 'container_detail.html', {'container': container, 'review_statistics': review_statistics})


