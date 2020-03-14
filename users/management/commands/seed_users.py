from django.core.management.base import BaseCommand
from rooms import models as room_models
from users import models as user_models
from django_seed import Seed


NAME = "users"


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

        inserted_pks = seeder.add_entity(
            user_models.User, number, {"is_staff": False, "is_superuser": False}
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"We saved {number} {NAME}."))
