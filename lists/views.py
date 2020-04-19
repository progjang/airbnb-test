from django.shortcuts import redirect, reverse
from . import models
from rooms import models as room_models
from django.views.generic import TemplateView

# Create your views here.


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            name="My Favourite Rooms", user=request.user
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class FavTemplateView(TemplateView):
    model = models.List
    template_name = "lists/list_detail.html"
