from django.shortcuts import render

# Create your views here.

def login_page(request):
    return render(request, 'chat/login.html')


def register_page(request):
    return render(request, 'chat/register.html')
