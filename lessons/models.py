from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger('lessons')

SUBSCRIPTION_TIPES = (
    ("Lezioni", "Lezioni"),
    ("Mensile", "Mensile")
)

class Lesson(models.Model):
    date = models.DateField(verbose_name=_('Data'))
    cost = models.IntegerField(default=1, verbose_name=_('Costo'))
    guests = models.CharField(null=True, max_length=1024, blank=True, verbose_name=('Ospiti'))
    participants = models.ManyToManyField('Person', blank=True, verbose_name=_('Partecipanti'))

    class Meta:
        verbose_name = _('Lezione')
        verbose_name_plural = _('Lezioni')

    def __str__(self):
        return _('Lezione del %(date)s') % {'date': self.date}
    

class Person(models.Model):
    name = models.CharField(max_length=1024, verbose_name=_('Nome'))
    availableLessons = models.IntegerField(default=0, verbose_name=_('Lezioni disponibili'))
    subscriptionType = models.CharField(choices=SUBSCRIPTION_TIPES, max_length=16, verbose_name=_('Tipologia abbonamento'))
    subscriptionStart = models.DateField(null=True, blank=True, verbose_name=_('Data inizio abbonamento'))
    archived = models.BooleanField(default=False, verbose_name=_('Archiviato'))
    #lessons = models.ManyToManyField(Lesson, blank=True, verbose_name=_('Lezioni partecipate'))

    class Meta:
        verbose_name = _('Iscritto')
        verbose_name_plural = _('Iscritti')

    def __str__(self):
        return self.name


@receiver(m2m_changed, sender=Lesson.participants.through)
def on_lesson_created(sender, instance, action, reverse, pk_set, **kwargs):
    cost = instance.cost
    if action == "post_add":
        persons_to_add = Person.objects.filter(pk__in=pk_set)
        for person in persons_to_add:
            if person.subscriptionType == "Lezioni":
                logger.info("A causa di una modifica alla lezione " + str(instance) + " rimuovo " + str(cost) + " lezioni dall'utente " + str(person))
                person.availableLessons -= cost
                person.save()

    elif action == "post_remove":
        persons_to_remove = Person.objects.filter(pk__in=pk_set)
        for person in persons_to_remove:
            if person.subscriptionType == "Lezioni":
                logger.info("A causa di una modifica alla lezione " + str(instance) + " aggiungo " + str(cost) + " lezioni dall'utente " + str(person))
                person.availableLessons += cost
                person.save()
       
