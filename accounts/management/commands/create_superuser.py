from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'adminpassword123'  # You should change this to a secure password
        
        try:
            # Check if superuser already exists
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists. No new superuser created.'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'Could not create superuser. User "{username}" may already exist.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
