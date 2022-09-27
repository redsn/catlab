from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from .models import Cat, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'cat-collector-seir-426-assets-426'

# Create your views here.

def home(request):
    return render(request, 'home.html', {'pageName': 'Home'})

# def contact(request):
#     return HttpResponse('Admin: contact@email.box<a href="/contact">???</a>')

# def test(request):
#     return HttpResponse('Nah <a href="/">BACK TO HOME</a>')

def about(request):
    return render(request, 'about.html', {'pageName': 'About'})

@login_required
def cats_index(request):
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {'cats': cats, 'pageName': 'Index'})

@login_required
def cats_detail(request,cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    # toys_cat_doesnt_have = cat.toys.all().values_list('id')
    # print(toys_cat_doesnt_have)
    return render(request, 'cats/detail.html', {'cat': cat, 'feeding_form': feeding_form, 'pageName': 'Cat Detail', 'toys_cat_doesnt_have': toys_cat_doesnt_have})

@login_required
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

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    # Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat_detail', cat_id=cat_id)

def signup(request):
    ## Define two branches of logic, 
    # ##Tasks for POST requests, 
    form = UserCreationForm()
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat_index')
    # Capture form inputs from the user creation form and validate. Then save input values as a new user to database
    ## Programatically login user then redirect user to cats index page
    # if form is invalid, show error message
    # render a template with an empty form
    # ##Tasks for GET requests
        else:
            error_message = 'invalid login/cruedentials'
    context = {'form': form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context )

def add_photo(request, cat_id):
    # Capture the photo file from our form submission
    photo_file = request.FILES.get('photo-file')
    # check if a file present
    if photo_file:
        # initialize the boto3 s3 service
        s3 = boto3.client('s3')
        # create a unique id for each photo file
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # attempt to upload the file assest to aws s3
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # generate a url based on the return value
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            # associate the cat to the new photo instance
            photo = Photo(url=url, cat_id=cat_id)
            photo.save()
            # store the url in the database -> in photo url attribute
        except Exception as error:
            print(f'An error occured while uploading: {error}')
    return redirect('cat_detail', cat_id=cat_id)    

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ('name', 'breed', 'description', 'age')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    # success_url = '/cats/'

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ('age', 'breed', 'description')

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
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
