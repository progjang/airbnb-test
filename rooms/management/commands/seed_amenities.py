from django.core.management.base import BaseCommand
from rooms import models as room_models

NAME = "Amenities"


class Command(BaseCommand):

    help = ""

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want to make?",
        )

    def handle(self, *args, **options):
        number = options.get("number")

        list_facilities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop-friendly workspace",
            "TV",
            "Crib",
            "High chair",
            "Self check-in",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Private bathroom",
            "Beachfront",
            "Waterfront",
            "Ski-in/ski-out",
        ]

        for a in list_amenities:
            print(a)
            room_models.Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS(f"We saved {number} {NAME}."))
