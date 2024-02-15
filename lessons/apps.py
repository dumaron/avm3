from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LessonsConfig(AppConfig):
    name = 'lessons'
    verbose_name = _('Lezioni di Yoga')
