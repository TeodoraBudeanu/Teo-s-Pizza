from django.shortcuts import render, redirect

def welcome(request):
    if request.user.is_authenticated:
        return redirect('client_home')
    return render(request, 'pizza/welcome.html')
