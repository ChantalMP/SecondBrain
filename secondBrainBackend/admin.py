from django.contrib import admin

# Register your models here.
from .models import ImageData,NoteData

admin.site.register(NoteData)