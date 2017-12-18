from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def success(request):
    try:
        context = {
            "user": User.objects.get(id = request.session['id']).first_name
        }
        return render(request, "first_app/success.html", context)
    except:
        return redirect('/')


def login(request):
    result = User.objects.login_val(request.POST)
    if type(result) == dict:
        for error in errors.itervalues():
            messages.error(request, error, extra_tags="reg")
        return redirect('/')
    
    request.session['id'] = User.objects.get(email= request.POST['email']).id
    return redirect('/success')

def register(request):
    errors = User.objects.register_val(request.POST)
    if errors:
        for error in errors.itervalues():
            messages.error(request, error, extra_tags="reg")
        return redirect("/")

    password = request.POST["password"]
    hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5)) 
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST["last_name"],email = request.POST["email"], password = hashed)
   
    request.session['id'] = user.id
    return redirect('/success')


    
def logout(request):
    request.session.clear()
    return redirect('/')
