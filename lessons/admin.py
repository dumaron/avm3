from django.contrib import admin
from .models import Person, Lesson
from django.utils.translation import gettext as _
from django.utils.html import format_html
from django.urls import reverse


admin.site.index_title = _('Pannello di amministrazione')
admin.site.site_header = _('Atma Vichara Manager 3')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'availableLessons', 'stato', 'subscriptionType']
    exclude = ['archived', 'deleted']
    search_fields = ['name']
    readonly_fields = ['Lezioni']
    list_filter = ['archived', 'subscriptionType']
    # exclude = ['lessons']

    def Lezioni(self, obj):        
        base = '<ul class="no-space">'
        for lesson in obj.lesson_set.all():
            link = reverse("admin:lessons_lesson_change", args=[lesson.id])
            base += f'<li><a href="{link}">{lesson}</a></li>'
        return format_html(base + '</ul>')

    def stato(self, obj):
        color = 'lesson-number'
        text = 'Mensile'
        if (obj.subscriptionType == 'Lezioni'):
            text = 'Sicuro'
            color += ' success'
            if (obj.availableLessons < 3):
                text = 'Rinnovo'
                color += ' danger'
            elif (obj.availableLessons < 5):
                text = 'Attenzione'
                color += ' warning'

        return format_html(f'<div class="{color}">{text}</div>')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    autocomplete_fields = ['participants']
