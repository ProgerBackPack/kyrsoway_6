from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания пользователей
    """
    def handle(self, *args, **options):
        user_list = [
            {"email": "test1@test.ru", "first_name": "Ivan", "last_name": "Ivanov", "is_active": True,},
            {"email": "test2@test.ru", "first_name": "Petr", "last_name": "Petrov", "is_active": True,},
            {"email": "test3@test.ru", "first_name": "Semen", "last_name": "Semenov", "is_active": True,},
            {"email": "test4@test.ru", "first_name": "Mix", "last_name": "Mixov", "is_active": True,},
        ]
        user_for_create = []
        for item in user_list:
            user_for_create.append(User(**item))
            user_for_create[-1].set_password("12345qwerty")

        User.objects.bulk_create(user_for_create)