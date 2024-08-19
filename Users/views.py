from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your request has been submitted! Please wait for activation!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'Users/profile.html', {'form': form})

def pw_reset_done(request):
    messages.success(request, f'Your request has been submitted!')
    return redirect('login')

def pw_reset_complete(request):
    messages.success(request, f'Your password has been reset!')
    return redirect('login')
