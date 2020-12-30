from django.contrib import admin

from .models import Query, Option, Attendee, Choice


class OptionInline(admin.StackedInline):
    model = Option
    extra = 1


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [OptionInline]


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'query', 'option', 'status')
    list_display_links = ('attendee', 'query', 'option', 'status')
    list_filter = ('attendee', 'option__query')

    def query(self, obj):
        return obj.option.query
