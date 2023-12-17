from django.core.management.base import BaseCommand
from activities.factories import ActivityFactory


class Command(BaseCommand):
    help = "Creates fake activities."

    def add_arguments(self, parser):
        parser.add_argument("num", type=int, help="Number of activities to create")

    def handle(self, *args, **options):
        """Create a number of fake activities."""
        if options["num"] >= 0:
            for _ in range(options["num"]):
                ActivityFactory.create()
            self.stdout.write(f"Created {options['num']} fake activities.")
            return

        self.stdout.write("Invalid n. Please try again.")