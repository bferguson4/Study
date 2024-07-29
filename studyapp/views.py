from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import StudySet, Flashcards
from .forms import StudySetForm, FlashcardsForm
from django.db.utils import IntegrityError
from django.http import HttpRequest


# Creates the view for the homepage
def main_view(request):
    return main_view_help(request, {})

def main_view_help(request, context):
    study_form = StudySetForm(request.POST or None)

    if study_form.is_valid(): 
        study_form.save() 

    study_sets = StudySet.objects.all()
    context["form"] = study_form
    context["study_sets"] = study_sets
    
    return render(request, "main.html", context)

# Creates the view for flashcard creation
def create_view(request, set_id): 
    context ={} 
    
    flashcards_form = FlashcardsForm(request.POST or None)
    if flashcards_form.is_valid():
        flashcards_form.instance.set_id = set_id
        flashcards_form.instance.difficulty = "Hard"
        flashcards_form.save()
        flashcards_form = FlashcardsForm()
    

    context['flashcards'] = Flashcards.objects.filter(set=set_id)
    context['flashcards_form'] = flashcards_form
    context['set_id'] = set_id

    return render(request, "studyset_form.html", context)  

# Deletes a specific flashcard
def delete_flashcard(request):
    flashcard_id = request.POST.get("delete_button")
    flashcard = Flashcards.objects.get(id = flashcard_id)
    set_id = flashcard.set.id
    flashcard.delete()
    
    return redirect("create", set_id = set_id)

# Deletes a specific set
def delete_set(request):
    set_id = request.POST.get("delete")
    if (set_id != 'NaN'):
        set = StudySet.objects.get(id = set_id)
        try:
            set.delete()
        except IntegrityError:
            if (request.POST.get("yes") != None):
                flashcards_to_delete = Flashcards.objects.filter(set = set_id)
                for flashcard in flashcards_to_delete:
                    flashcard.delete()
                set.delete()
            else:
                context = {}
                context['flashcards'] = Flashcards.objects.filter(set=set_id)
                context['set_id'] = set_id
                return render(request, "delete_set.html", context)
            
    return redirect("main")


# Creates the view for practicing viewing the flashcard
def practice_flashcards(request, set_id):
    context ={}

    context['flashcards'] = Flashcards.objects.filter(set=set_id)
    context['set_id'] = set_id

    return render(request, "flashcards.html", context)

# Creates the view for the learn activity
def learn(request, set_id):
    context = {}
    flashcard = get_flashcard(set_id)
    if (request.method == "POST"):
        if (flashcard == None):
            reset_flashcard_diff()
            flashcard = get_flashcard(set_id)
        else:
            flashcard.difficulty = request.POST.get('button_value')
            flashcard.save()
            flashcard = get_flashcard(set_id)
    context['flashcard'] = flashcard
    context['set_id'] = set_id

    return render(request, "learn.html", context)

# Chooses the next flashcard for the learn activity
def get_flashcard(set_id) -> Flashcards:
    try:
        flashcard = Flashcards.objects.filter(set=set_id, difficulty="Hard").earliest('modified')
    except Flashcards.DoesNotExist:
        flashcard = None
    return flashcard

# Reset all the difficulties to hard for flashcards
def reset_flashcard_diff():
    flashcards = Flashcards.objects.all()
    for flashcard in flashcards:
        flashcard.difficulty = "Hard"
        flashcard.save()
        
# Creates the view for editing flashcards
def edit_view(request, flashcard_id):
    context = {}
    flashcard = Flashcards.objects.get(id = flashcard_id)
    
    if request.method == "POST":
        form = FlashcardsForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
    
    context['flashcard_id'] = flashcard_id
    context['set_id'] = flashcard.set.id
    context['flashcard'] = flashcard

    return render(request, "edit.html", context)

