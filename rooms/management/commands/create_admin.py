import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Tạo Django superuser nếu chưa tồn tại'

    def handle(self, *args, **options):

        User = get_user_model()

        username = os.environ.get(
            'DJANGO_SUPERUSER_USERNAME'
        )

        email = os.environ.get(
            'DJANGO_SUPERUSER_EMAIL'
        )

        password = os.environ.get(
            'DJANGO_SUPERUSER_PASSWORD'
        )

        if not username:
            self.stdout.write(
                self.style.ERROR(
                    'Thiếu DJANGO_SUPERUSER_USERNAME'
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    'Thiếu DJANGO_SUPERUSER_PASSWORD'
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email or '',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        if created:
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Đã tạo superuser: {username}'
                )
            )

        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser đã tồn tại: {username}'
                )
            )