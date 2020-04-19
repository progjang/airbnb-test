import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def room_booked(room, date):
    if date.date == 0:
        return
    try:
        date = datetime.date(year=date.year, month=date.month, day=date.date)
        reservations = reservation_models.Reservation.objects.filter(room=room)
        for reservation in reservations:
            if reservation.check_in <= date and date <= reservation.check_out:
                return True
    except reservation_models.Reservation.DoesNotExist:
        return False


@register.simple_tag
def is_booked(room, date):
    if date.date == 0:
        return
    try:
        day = datetime.datetime(year=date.year, month=date.month, day=date.date)
        reservation_models.BookedDay.objects.get(date=day, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoewsNotExist:
        return False
