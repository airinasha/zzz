from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        full_name = request.user.get_full_name()
        gps = request.user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts,'fname': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author.')
            user_signup = form.save()
            group = Group.objects.get(name='Author')
            user_signup.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successgully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                des = form.cleaned_data['desc']
                pst = Post(title=title, desc=des)
                pst.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


