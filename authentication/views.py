from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from members.models import Member
from .models import *

@login_required 


def home(request):
	return render(request, 'welcome.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login_page')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login_page')
        else:
            login(request, user)
            return redirect('welcome')

    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        username = (request.POST.get('username') or '').strip().lower()
        password = request.POST.get('password')

        try:
            validate_email(username)
        except DjangoValidationError:
            messages.error(request, "Enter a valid email.")
            return redirect('register')
        
        password_errors = []
        if len(password) < 8:
            password_errors.append("Password must be at least 8 characters long.")  
        if password.isdigit():
                password_errors.append("Password can't be entirely numeric.")
        if password.lower() in [first_name.lower(), last_name.lower(), username.split('@')[0]]:
                password_errors.append("Password is too similar to your personal information.") 
        if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
                password_errors.append("Password must contain both letters and digits.")
        if not all(char.isalnum() or char in '@./+/-/_' for char in password):
                password_errors.append("Password contains invalid characters. Only letters, digits and @/./+/-/_ are allowed.")
        if password_errors:
            messages.error(request, " ".join(password_errors))
            return redirect('register')


        member = Member.objects.filter(email__iexact=username).first()
        if member is None:
            messages.error(
                request,
                "Registration is allowed only for club members. Contact the administrator to add your email to the membership.",
            )
            return redirect('register')

        # Identity verification - first name/last name must match the member
        if (member.firstname or '').strip().lower() != first_name.lower() or (member.lastname or '').strip().lower() != last_name.lower():
            messages.error(request, "First name or last name does not match the registered member.")
            return redirect('register')

        if member.user_id is not None:
            messages.info(request, "This member already has an account. Try logging in.")
            return redirect('login_page')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=username,
            password=password
        )

        member.user = user
        if not member.email:
            member.email = username
        member.save(update_fields=['user', 'email'])

        messages.success(request, "Account has been successfully created! Please log in.")
        return redirect('login_page')

    return render(request, 'register.html')
