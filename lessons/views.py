from django.http import HttpResponse
from django.template import loader
from .models import Person

def index(request):
    persons = Person.objects.filter(archived=False, subscriptionType="Lezioni").order_by("availableLessons")
    template = loader.get_template('index.html')
    context = {
        'persons': persons
    }
    return HttpResponse(template.render(context, request))