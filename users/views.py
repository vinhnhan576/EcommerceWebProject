from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = RegisterForm()

    return render(
        request=request,
        template_name="register.html",
        context={"form": form}
    )


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required    
def logout_user(request):
    logout(request)
    return redirect('/')
    
