from django.contrib import admin
from django.urls import path, include
from studyapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main_view, name='main'),
    path('set/<set_id>/', views.create_view, name='create'),
    path('flashcards/<set_id>/', views.practice_flashcards, name='flashcards'),
    path('learn/<set_id>/', views.learn, name='learn'),
    path('edit/<flashcard_id>/', views.edit_view, name='edit'),
    path('delete_flashcard/', views.delete_flashcard, name='delete_flashcard'),
    path('delete_set/', views.delete_set, name='delete_set')
]

