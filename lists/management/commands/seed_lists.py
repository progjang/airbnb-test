import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from users import models as user_models
from rooms import models as room_models
from lists import models as list_models
from django_seed import Seed


NAME = "reviews"


class Command(BaseCommand):

    help = f"This command will create some {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")

        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(all_users)},
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))

        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            added_room = all_rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*added_room)
        self.stdout.write(self.style.SUCCESS(f"We saved {number} {NAME}."))
