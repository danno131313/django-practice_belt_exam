from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Comment
import bcrypt

def index(request):
    if loggedIn(request):
        return redirect('/show')
    else:
        return render(request, "practice_app/index.html")

def create_user(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    
    User.objects.create_user(request.POST)
    messages.success(request, "User " + request.POST['first_name'] + " has been created! Please log in")

    return redirect('/')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "That user cannot be found")
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.success(request, "You have been successfully logged in")

        request.session['id'] = user.id
        request.session['email'] = user.email
        request.session['name'] = user.first_name

        return redirect('/show')

    else:
        messages.error(request, "Password was incorrect")
        return redirect('/')

def logout(request):
    logout_user(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('/')

def show(request):
    if not loggedIn(request):
        messages.error(request, "You must be logged in to do that")
        return redirect('/')
    
    context = {
        'users': User.objects.exclude(id=request.session['id']),
    }

    return render(request, 'practice_app/show.html', context)

def show_one(request, id):
    if not loggedIn(request):
        messages.error(request, "You must be logged in to do that")
        return redirect('/')

    user = User.objects.get(id=id)

    context = {'user': user}
    return render(request, 'practice_app/show_one.html', context)

def create_comment(request, id):
    if not loggedIn(request):
        messages.error(request, "You must be logged in to do that")
        return redirect('/')
    poster = User.objects.get(id=request.session['id'])
    recipient = User.objects.get(id=id)
    comment = Comment.objects.create(content=request.POST['comment'], poster=poster, recipient=recipient)
    
    messages.success(request, "Comment created successfully")
    return redirect('/users/' + str(id) + "/show")

def loggedIn(request):
    return 'id' in request.session

def checkLogin(request):
    if not loggedIn(request):
        messages.error(request, "You must be logged in to do that")
        return redirect('/')
    else:
        print("logged in")

def logout_user(request):
    request.session.flush()
