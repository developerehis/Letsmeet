from django.shortcuts import render,redirect
from .forms import UserLoginForm, RegisterForm, ProfileEditForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Profile
from .utils import from_label_to_value

# Create your views function for index page.
def index(request):
    users = Profile.objects.all() # variable to get all user from hhe model/Database
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        users = Profile.objects.exclude(user=request.user) # exclude login user
    else:
        profile = ''

    context = { #pass vairable to the index page
        'profile': profile,
        'users': users,
    }
    return render(request, 'pages/index.html', context)

def search(request):
    query = request.GET.get('speaks').replace(" ","") # Get all vairable that is passed to the url search box and delete all empty spaces
    list_speaks = query.split(',')
    
    if user.is_authenticated:
        profile = Profile.objects.get(user=request.user) # Profile variable to fetch all users
        results = Profile.objects.exclude(id=profile.id).filter(speaks__icontains=list_speaks[0])
    else:
        profile = ''
        results = Profile.objects.filter(speaks__icontain=list_speaks[0])

    return render(request, 'pages/index.html')

# Create your views function for profile  page.
def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    context = {
        'profile': profile
    }
    return render(request, 'pages/profile.html', context)

def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.speaks = form.from_value_to_label('speaks')
            obj.is_learning = form.from_value_to_label('is_learning')
            obj.save()
            messages.success(request, "Profile updated successfully")
            return redirect('pages:profile', profile_id=request.user.profile.id)
    else:
        is_learning = from_label_to_value(request, 'is_learning')
        speaks = from_label_to_value(request, 'speaks')
        form = ProfileEditForm(instance=request.user.profile, initial={'is_learning': is_learning, 'speaks': speaks})
    return render(request, 'pages/edit.html',{'form':form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                do_login(request,user)
                return redirect('pages:index')
            else:
                return redirect('pages:login')
    else:
        form = UserLoginForm()
    return render(request, 'pages/login.html',{'form':form})

def logout(request):
    do_logout(request)
    return redirect('pages:login')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Created Successfully!')
            return redirect('pages:login')
        else:
            messages.error(request, 'An error ocurred')
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html',{'form':form})


