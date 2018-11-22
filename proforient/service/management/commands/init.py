from django.core.management.base import BaseCommand, CommandError
from service.models import Categories


class Command(BaseCommand):
    help = "This command initialize database"

    def handle(self, *args, **options):
        self.create_categories()

    def create_categories(self):
        categories_name = ['lecture', 'consultation', 'testing', 'tutoring', 'event']
        categories_slug = ['Лекция', 'Консультация', 'Тестирование', 'Репетиторство', 'Мероприятие']

        for i in range(len(categories_name)):
            cat = Categories()
            cat.name = categories_name[i]
            cat.slug = categories_slug[i]
            cat.save()
