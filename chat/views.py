from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from urllib.parse import uses_netloc
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Message
from .models import FriendRequest
import smtplib
import string
import re
import os

# chat page
@login_required
def chat_page(request):
    friends = User.objects.filter(
        sent_requests__receiver=request.user,
        sent_requests__accepted=True
    ) | User.objects.filter(
        received_requests__sender=request.user,
        received_requests__accepted=True
    )

    return render(request, "chat/chat.html", {
        "users": friends.distinct()
    })

@login_required
def send_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        note = request.POST.get("note")   # 👈 ADD THIS

        try:
            receiver = User.objects.get(username=username)

            if receiver == request.user:
                return JsonResponse({"error": "Cannot add yourself"})

            FriendRequest.objects.get_or_create(
                sender=request.user,
                receiver=receiver,
                defaults={"note": note}   # 👈 SAVE NOTE
            )

            return JsonResponse({"success": "Request sent"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"})

@login_required
def accept_request(request, request_id):
    req = FriendRequest.objects.get(id=request_id, receiver=request.user)
    req.accepted = True
    req.save()

    return redirect("request_page")


@login_required
def request_page(request):
    requests = request.user.received_requests.filter(accepted=False)
    return render(request, "chat/requests.html", {
        "requests": requests
    })

# contact page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").lower().strip()
        password = request.POST.get("password", "").strip()

        if not User.objects.filter(username=username).exists():
            messages.warning(request, "Username does not exist.")
            return redirect("login_page")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'chat/about.html', {"username": username})

        else:
            messages.warning(request, "Incorrect password.")
            return redirect("login_page")

    return render(request, 'chat/login.html')


# register page
def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").lower().strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if len(username) < 3:
            messages.warning(request, "Username must be at least 3 characters long.")

        elif len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters long.")

        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!%*#?&_]{8,}$', password):
            messages.warning(request, "Password must contain a letter, a number, and a symbol.")

        elif not all(ch in (string.ascii_lowercase + string.digits + "_") for ch in username):
            messages.warning(request, "Username can only contain lowercase letters, numbers, and underscores.")

        elif password != confirm_password:
            messages.warning(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists!")

        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect("login_page")  # Redirect to login on success

        return render(request, 'chat/register.html', {"username": username})

    return render(request, 'chat/register.html')


# contact page
@login_required(login_url="login_page")
def contact_page(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").lower().strip()
        username = request.POST.get("username", "").lower().strip()
        context = request.POST.get("user_message_box", "").lower()

        if not User.objects.filter(username=username).exists():
            messages.warning(request, "Username does not exist.")
            return redirect("contact_page")

        email = os.getenv("MY_EMAIL")
        password = os.getenv("MY_PASSWORD")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs="ayaancoder77@gmail.com",
                msg=f"Subject: {full_name.title()} message from SoulSyn Username: {username}\n\n{context}"
            )

        messages.success(request, 'Email sent successfully!')
        return redirect("contact_page")

    return render(request, 'chat/contact.html')


# about page
def about_page(request):
    return render(request, 'chat/about.html')


# logout page
@login_required(login_url="login_page")
def logout_page(request):
    logout(request)
    return redirect("login_page")