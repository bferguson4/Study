from django.contrib import admin
from .models import Flashcards, StudySet

# Register your models here.
@admin.register(Flashcards)
class FlashcardsAdmin(admin.ModelAdmin):
    pass

@admin.register(StudySet)
class StudySetAdmin(admin.ModelAdmin):
    pass

