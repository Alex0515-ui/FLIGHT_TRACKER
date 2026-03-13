from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  # Готовая пользовательская модель

    def __str__(self):
        return f"user id:{self.pk}, username: {self.username}"
