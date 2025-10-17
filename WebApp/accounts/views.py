from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # 👈 creates user in the database
            return redirect('login')  # you can redirect wherever you want
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
