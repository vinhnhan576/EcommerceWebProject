from django.shortcuts import render
from .forms import RegisterForm

def register_user(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'register.html', context)

