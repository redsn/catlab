from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from .models import Cat, Toy
from .forms import FeedingForm

# Create your views here.

def home(request):
    return render(request, 'home.html', {'pageName': 'Home'})

# def contact(request):
#     return HttpResponse('Admin: contact@email.box<a href="/contact">???</a>')

# def test(request):
#     return HttpResponse('Nah <a href="/">BACK TO HOME</a>')

def about(request):
    return render(request, 'about.html', {'pageName': 'About'})


def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats, 'pageName': 'Index'})

def cats_detail(request,cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {'cat': cat, 'feeding_form': feeding_form, 'pageName': 'Cat Detail'})

def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat_detail', cat_id=cat_id)

def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys, 'pageName': 'Toy Index'})

def toy_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, 'toys/detail.html', {'toy': toy, 'pageName': 'Toy details'})


class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # success_url = '/cats/'

class CatUpdate(UpdateView):
    model = Cat
    fields = ('age', 'breed', 'description')

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'




## Alternatively fields can be decared with tuples or  lists. fields = ['field1', 'field2', etc] or = ('field1', 'field2', 'field3')
## Value of fields attribute is used to create a model form... Model forms are used byh Django to create html5 forms in order to create model instances
# """
# Adding a mock database:

"""
class clasname(ModelFormMixin, ProcessFormView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)
"""
# """

# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# cats = [
#     Cat('Lolo', 'tabby', 'foul demonspawn', 5),
#     Cat('Ben Johnson', 'doll', 'fluffy, rude', 3),
#     Cat('Miss Kitty', 'dalmation', 'cat*', 2)
# ]
