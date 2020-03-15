from django.shortcuts import render
from django.views.generic import DetailView
from . import models


class RoomDetail(DetailView):
    model = models.Room

