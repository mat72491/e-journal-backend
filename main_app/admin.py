from django.contrib import admin
from .models import JournalEntry, Tag
# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(Tag)