from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания superuser'a
    """
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@example.com',
            first_name='Admin',
            last_name='God',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password('291094')
        user.save()