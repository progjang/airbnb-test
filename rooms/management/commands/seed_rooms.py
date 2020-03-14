import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from rooms import models as room_models
from users import models as user_models

from django_seed import Seed


NAME = "rooms"


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
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        inserted_rooms = seeder.execute()
        print(inserted_rooms)
        cleaned_list = flatten(list(inserted_rooms.values()))
        print(cleaned_list)
        for pk in cleaned_list:
            room = room_models.Room.objects.get(pk=pk)
            photo_count = random.randint(3, 15)
            for p in range(1, photo_count):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"room_photos/photos_seed/{random.randint(1,32)}.webp",
                    room=room,
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"We saved {number} {NAME}."))
