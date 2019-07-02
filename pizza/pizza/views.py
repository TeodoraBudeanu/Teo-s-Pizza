from django.shortcuts import render, redirect

def welcome(request):
    return render(request, 'pizza/welcome.html')
