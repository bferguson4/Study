from django.db import models

# Create your models here.
class StudySet(models.Model):
    name = models.CharField(max_length = 400)

class Flashcards(models.Model):
    question = models.TextField()
    answer = models.TextField()
    set = models.ForeignKey(StudySet, on_delete=models.DO_NOTHING)
    difficulty = models.CharField(max_length=100)
    modified = models.DateTimeField(auto_now=True)