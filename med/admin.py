from django.contrib import admin

# Register your models here.
from .models import *

class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'time_create', 'time_update')
    list_display_links = ('word', 'translation')
    list_filter = ('word', 'time_create')
    search_fields = ('word', 'translation')

class WordGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_main')
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(Word, WordAdmin)
admin.site.register(WordGroup, WordGroupAdmin)