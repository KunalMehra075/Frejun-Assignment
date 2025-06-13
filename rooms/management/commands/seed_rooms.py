from django.core.management.base import BaseCommand
from rooms.models import Room

class Command(BaseCommand):
    help = 'Seed the database with initial rooms.'

    def handle(self, *args, **options):
        Room.objects.all().delete()
        # 8 Private Rooms
        for i in range(1, 9):
            Room.objects.create(
                room_type='PRIVATE',
                capacity=1,
                room_number=f'P{i}'
            )
        # 4 Conference Rooms
        for i in range(1, 5):
            Room.objects.create(
                room_type='CONFERENCE',
                capacity=20,  # Arbitrary large number, logic will enforce min 3
                room_number=f'C{i}'
            )
        # 3 Shared Desks (each allows up to 4 users)
        for i in range(1, 4):
            Room.objects.create(
                room_type='SHARED',
                capacity=4,
                room_number=f'S{i}'
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded 15 rooms.')) 