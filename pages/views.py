from django.shortcuts import render,redirect
from .forms import UserLoginForm, RegisterForm, ProfileEditForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Profile, FriendRequest
from .utils import from_label_to_value, sort
from django.core.paginator import Paginator

# Create your views function for index page.
def index(request):
    users = Profile.objects.all() # variable to get all user from hhe model/Database
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        users = Profile.objects.exclude(user=request.user) # exclude login user
    else:
        profile = ''
    #print(profile.coming_from_profile.all())
    #print(profile.to_profile.all())
    # pagination variables
    page_num =  request.GET.get('page')
    paginator = Paginator(users, 8)
    page_obj = paginator.get_page(page_num)

    context = { #pass vairable to the index page
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'pages/index.html', context)

def search(request):
    query = request.GET.get('speaks').replace(" ","") # Get all vairable that is passed to the url search box and delete all empty spaces
    query2 = request.GET.get('learning').replace(" ","") # Get all vairable that is passed to the url search box and delete all empty spaces

    list_speaks = query.split(',')
    list_learning = query2.split(',')
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user) # Profile variable to fetch all users
        results = Profile.objects.exclude(id=profile.id).filter(speaks__icontains=list_speaks[0]).filter(le_learning__icontains=list_learning[0])
    else:
        profile = ''
        results = Profile.objects.filter(speaks__icontains=list_speaks[0]).filter(is_learning__icontains=list_learning[0])
    
    results = sort(elements=list_speaks, results=results, l_s=True)
    results = sort(elements=list_learning, results=results, l_l=True)

    # pagination variables
    page_num =  request.GET.get('page')
    paginator = Paginator(results, 1)
    page_obj = paginator.get_page(page_num)

    s = f"speaks={request.GET.get('speaks')}&learning={request.GET.get('learning')}&"

    # context dictionary to pass variable to the index page
    context = {
        'profile' : profile,
        'page_obj' : page_obj,
        's':s,
    }
    return render(request, 'pages/index.html', context)

# Create your views function for profile  page.
def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    friends = profile.friends.all()
    received_requests = FriendRequest.objects.filter(to_profile=profile)

    btn_text = ''
    if request.user.is_authenticated:
        if profile not in request.user.profile.friends.all():
            btn_text = 'not_friend'
            if len(FriendRequest.objects.filter(from_profile=request.user.profile).filter(to_profile=profile))==1:
                btn_text = 'request_sent'

    context = {
        'profile': profile,
        'friends': friends,
        'received_requests': received_requests,
        'btn_text': btn_text
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

def send_request(request, to_profile_id):
    if request.user.is_authenticated:
        to_profile = Profile.objects.get(pk=to_profile_id)
        frequest = FriendRequest.objects.get_or_create(
            from_profile = request.user.profile,
            to_profile = to_profile
        )
        return redirect('pages:profile', profile_id=to_profile.id)

def cancel_request(request, to_profile_id):
    if request.user.is_authenticated:
        to_profile = Profile.objects.get(pk=to_profile_id)
        frequest = FriendRequest.objects.filter(
            from_profile = request.user.profile,
            to_profile = to_profile
        ).first()

        frequest.delete()
        
        return redirect('pages:profile', profile_id=to_profile.id)

