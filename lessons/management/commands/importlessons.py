from django.core.management.base import BaseCommand, CommandError
from lessons.models import Person
import json

class Command(BaseCommand):
    help = 'Importa gli iscritti allo studio'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['json_file'][0]
        with open(path) as json_file:
            data = json.load(json_file)
            for lesson in data:
                print(lesson)
                #p = Lesson(
                #    name=person['name'], 
                #    archived=person['disabled'] if 'disabled' in person else True, 
                #    availableLessons=person['lessons'] if 'lessons' in person else 0,
                #    subscriptionType=('Lezioni' if person['subType'] == 'single' else 'Mensile')
                #    )
                #p.save()
                #print('Creato ' + str(p))