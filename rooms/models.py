import mycalendar
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils import timezone
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Facility(AbstractItem):
    """ Facility Class Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class Amenity(AbstractItem):
    """ Amenity Class Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class RoomType(AbstractItem):
    """ RoomType class Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["-created_at"]


class HouseRule(AbstractItem):
    """ HouseRule class Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """ Photo class Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos/%Y/%m/%d",)
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE,)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, on_delete=models.SET_NULL, related_name="rooms", blank=True, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    def review_average(self):
        total_rating = 0
        reviews = self.reviews.all()
        if reviews.count() == 0:
            avg = 0
        else:
            for review in reviews:
                total_rating += review.rating_average()
                avg = round(total_rating / len(reviews), 2)

        return avg

    review_average.short_description = "Reviews Avg."

    def first_photo(self):
        (photo,) = self.photos.all()[:1]
        return photo.file.url

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        current_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            current_year += 1
            next_month = 1

        this_month_calendar = mycalendar.Calendar(current_year, this_month)
        next_month_calendar = mycalendar.Calendar(current_year, next_month)
        return (this_month_calendar, next_month_calendar)
