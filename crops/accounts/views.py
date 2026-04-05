from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():  # ✅ Validation happens here
            form.save()  # saves user to DB
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'html/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard_home')  # 👈 redirect to main_dashboard home
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'html/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('login')


