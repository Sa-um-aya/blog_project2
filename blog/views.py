from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})



def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})




def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, "Account created successfully 🎉")
            return redirect('home')
        else:
            messages.error(request, "Signup failed. Please check details ❌")
    else:
        form = SignupForm()

    return render(request, 'blog/signup.html', {'form': form})





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill all fields ⚠️")
            return render(request, 'blog/login.html')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful 🎉")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, 'blog/login.html')

    return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')