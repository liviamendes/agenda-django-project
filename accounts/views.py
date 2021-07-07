from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact
from contacts.models import Contact


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Username or password is invalid')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'User logged in successfully.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not name or not last_name or not email or not username or not password or not password2:
        messages.error(request, 'NO FIELDS MUST BE EMPTY')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'INVALID EMAIL')
        return render(request, 'accounts/register.html')

    if len(password) < 8:
        messages.error(request, 'PASSWORD MUST HAVE MORE THAN 8 CHARACTERS')
        return render(request, 'accounts/register.html')

    if len(username) < 6:
        messages.error(request, 'USERNAME MUST HAVE MORE THAN 6 CHARACTERS')
        return render(request, 'accounts/register.html')

    if password != password2:
        messages.error(request, 'PASSWORDS MUST BE THE SAME')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'USER ALREADY EXISTS')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-MAIL ALREADY EXISTS')
        return render(request, 'accounts/register.html')

    messages.success(request, 'USER SUCCESSFULLY REGISTERED')
    user = User.objects.create_user(username=username, email=email, password=password, first_name=name,
                                    last_name=last_name)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def update_view(request, contact_id):
    context = {}
    obj = get_object_or_404(Contact, id=contact_id)
    form = FormContact(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('index')

    context["form"] = form
    return render(request, "accounts/update_view.html", context)


@login_required(redirect_field_name='login')
def delete(request, contact_id):
    context = {}
    obj = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        obj.delete()
        return redirect('index')

    return render(request, "accounts/delete.html", context)


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContact(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'Error submitting form.')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    email = request.POST.get('email')
    try:
        validate_email(email)
    except:
        messages.error(request, 'INVALID EMAIL')
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, 'USER SUCCESSFULLY REGISTERED!')
    return redirect('dashboard')
