from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from . import models


class RoomDetail(DetailView):
    model = models.Room


class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    page_kwargs = "page"
    ordering = "created_at"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
