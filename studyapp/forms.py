from django.forms import fields
from .models import StudySet, Flashcards
from django import forms

class StudySetForm(forms.ModelForm):  
  
    class Meta:  
        # To specify the model to be used to create form  
        model = StudySet  
        # It includes all the fields of model  
        fields = '__all__' 

class FlashcardsForm(forms.ModelForm):

    class Meta: 
        model = Flashcards
        fields = ['question', 'answer']