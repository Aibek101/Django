from django.shortcuts import render, redirect
from .models import Post, Category
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, SignInForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})