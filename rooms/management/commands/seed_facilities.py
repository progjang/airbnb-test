from django.core.management.base import BaseCommand
from rooms import models as room_models

NAME = "Facilities"


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
            "Free parking on premises",
            "Gym",
            "Hot tub",
            "Pool",
        ]

        for f in list_facilities:
            print(f)
            facilities = room_models.Facility.objects.create(name=f)

        self.stdout.write(
            self.style.SUCCESS(f"We saved {len(list_facilities)} {NAME}.")
        )
