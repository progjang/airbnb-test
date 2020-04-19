from django.shortcuts import render, Http404
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView
from . import models
from . import forms


class RoomDetail(DetailView):
    model = models.Room


class RoomPhotosView(DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    # def get_object(self, queryset=None):
    #     room = super().get_object(queryset=queryset)
    #     if room.host.pk != self.request.user.pk:
    #         raise Http404()
    #     return room


class EditRoomView(UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )


class HomeView(ListView):
    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    page_kwargs = "page"
    ordering = "created_at"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def search(request):

    filter_args = {}

    if request.method == "POST":
        form = forms.SearchForm(request.POST)
        print(request.POST)

        if form.is_valid():

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            print(price)
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            if city != "Anywhere":
                filter_args["city__startswith"] = city
            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type__pk"] = room_type

            if price is not None:
                filter_args["price__lte"] = price
            if guests is not None:
                filter_args["guests__gte"] = guests
            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms
            if beds is not None:
                filter_args["beds__gte"] = beds
            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for amenity in amenities:
                filter_args["amenities"] = amenity
            for facility in facilities:
                filter_args["facilities"] = facility

            rooms = models.Room.objects.filter(**filter_args)
            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})
