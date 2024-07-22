from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms

@login_required
def show_index(request):
    user = User.objects.get(username = request.user)
    context = {
        'user' : user,
        'posts' : Post.objects.filter(owner = request.user)
    }
    return render(request, 'index.html', context)

def user_index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts,
    }
    return render(request, 'user_index.html', context)

def show_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'User is already logged in...')
        return redirect('/') 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwrd')
        user_data = User.objects.get(username=username)

        auth = authenticate(username = username, password = password)
        if auth is not None:
            login(request, auth)
            messages.success(request, 'Logged in successfully')
            return redirect('/index/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/login/')

    context = {
        'login_form' : Login_form(),
    }
    return render(request, 'login.html', context)

def show_signup(request):
    if request.method == 'POST':
        new_fname = request.POST.get('fname')
        new_lname = request.POST.get('lname')
        # new_gender = request.POST.get('gender')
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_pwrd = request.POST.get('pwrd')

        new_user = User.objects.create(username = new_username, 
                                       first_name = new_fname, 
                                       last_name = new_lname, 
                                       email = new_email)
        new_user.set_password(new_pwrd)
        new_user.save()
        return render(request, 'signup.html', {'message': 'Account created Successfully!'})

    return render(request, 'signup.html')

@login_required(login_url='/login/')
def show_pwrdreset(request,):
    if request.method == 'POST':
        current_user = request.user
        new_pwrd0 = request.POST.get('npwrd')
        new_pwrd1 = request.POST.get('cpwrd')

        if len(new_pwrd0.strip()) < 8 and len(new_pwrd1.strip()) < 8:
            messages.error(request, 'Password should not be less than 8 characters')
            return redirect('/pwrdreset/')
        
        if new_pwrd0 != new_pwrd1:
            messages.error(request, 'Password mismatch!')
            return redirect('/pwrdreset/')
        

        current_user = User.objects.get(id = request.user.id)
        current_user.set_password(new_pwrd0)
        current_user.save()
        messages.success(request, 'Password changed successfully')
        
        
    return render(request, 'pwrdreset.html')

@login_required
def show_profile(request):
    user = request.user
    

    if request.method == 'POST':
        post_title = request.POST.get('post_title')
        post_body = request.POST.get('post_body')

        if post_body.strip() == '' and post_title.strip() == '':
            messages.error(request, 'Text field must not be empty')
            return redirect('/profile/')
        
        new_post = Post(post_title = post_title, post_body = post_body, owner = request.user)
        new_post.save()
        return redirect('/index/')
    
    posts_num = len(Post.objects.filter(owner = user))
    user_bio = UserBio.objects.get(owner = user)
    context = {
        'user' : user,
        'posts_num' : posts_num,
        'user_bio' : user_bio,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user = User.objects.get(username = request.user)
    user_bio = UserBio.objects.get(owner = user)

    if request.method == 'POST':
        # User model
        new_fname = request.POST.get('fname')
        new_lname = request.POST.get('lname')
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Bio model
        new_gender = request.POST.get('gender')
        new_age = request.POST.get('age')
        new_phone_num =request.POST.get('phone_num')
        new_country = request.POST.get('country')
        new_about = request.POST.get('about')

        user.first_name = new_fname
        user.last_name = new_lname
        user.email = new_email

        user_bio.gender = new_gender
        user_bio.age = new_age
        user_bio.phone_num = new_phone_num
        user_bio.country = new_country
        user_bio.about = new_about

        user.save()
        user_bio.save()
        messages.success(request, 'Profile Updated')
        return redirect('/profile/')
    
    context = {
            'user' : user,
            'user_bio' : user_bio,
        }
    return render(request, 'edit_profile.html',context)

@login_required
def show_logout(request):
    logout(request)
    messages.error(request, 'Logged out successfully')
    return redirect('/login/')

@login_required
def post_delete(request,id):
    post = Post.objects.get(id = id)
    post.delete()
    messages.success(request, 'Post Deleted successfully.')
    return redirect('/index/')

@login_required
def post_edit(request, id):
    
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        new_post_title = request.POST.get('post_title')
        new_post_body = request.POST.get('post_body')

        post.post_title = new_post_title
        post.post_body = new_post_body

        post.save()
        messages.success(request, 'Post updated')
        return redirect('/index/')
    context = {
        'post' : post,
    }
    return render(request,'profile.html', context)

def single_post(request, id):
    post = Post.objects.get(id = id)
    user_comment = Comment.objects.all().filter(post = post)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        email = request.POST.get('email')

        save_comment = Comment(post = post, comment = comment, email = email)
        save_comment.save()

        return redirect(f'/single-post/{id}/')
    context = {
        'comments' : user_comment,
        'post' : post,
    }
    return render(request, 'single_post.html', context)

class Login_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

# class ProfileEdit_form(forms.ModelForm):
#     class Meta:
#         model = UserBio
#         fields = ('')

# Create your views here.
