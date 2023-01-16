from django.core.management import BaseCommand
from django.contrib.auth.models import User

from core.models import Counter


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create(username='admin', email='admin@gmail.com')
            user.set_password('testpass123')
            user.save()

        counter, created = Counter.objects.get_or_create()
        if created:
            print("counter initialized....")
        print('----------------done-------------------')

