import datetime
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import Http404
from rooms import models as room_models
from reviews import forms as review_forms
from . import models

RESERVATION_DAYS = 1


class CreateError(Exception):
    pass


def create(request, room, year, month, date):
    try:
        date_obj = datetime.date(year, month, date)
        room = room_models.Room.objects.get(pk=room)
        existing_booked_day = models.BookedDay.objects.filter(
            date__range=(date_obj, date_obj + datetime.timedelta(days=RESERVATION_DAYS))
        ).exists()
        if existing_booked_day:
            raise CreateError()
        else:
            reservation = models.Reservation.objects.create(
                guest=request.user,
                room=room,
                check_in=date_obj,
                check_out=date_obj + datetime.timedelta(days=RESERVATION_DAYS),
            )
            return redirect(
                reverse("reservations:detail", kwargs={"pk": reservation.pk})
            )

    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request
        ):
            raise Http404()

        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/reservation_detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.guest != reservation.room.host
    ):
        raise Http404()

    if verb == "confirmed":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "canceled":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
