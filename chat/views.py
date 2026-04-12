from django.shortcuts import render

# Create your views here.

# contact page
def login_page(request):
    return render(request, 'chat/login.html')


# register page
def register_page(request):
    return render(request, 'chat/register.html')


# contact page
def contact_page(request):
    return render(request, 'chat/contact.html')

# about page
def about_page(request):
    return render(request, 'chat/about.html')
