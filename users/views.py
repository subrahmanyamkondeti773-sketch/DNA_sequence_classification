"""
Users app views - Register, Login, Logout, Profile.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import UserProfile


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to DNA Classification System, {user.username}! 🧬')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! 🧬')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)

    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """Display and edit user profile."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            # Update user fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            email = form.cleaned_data.get('email', '')
            if email:
                request.user.email = email
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    # Get user stats
    from dna_classifier.models import DNASequence
    predictions = DNASequence.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_predictions = DNASequence.objects.filter(user=request.user).count()

    context = {
        'form': form,
        'profile': profile,
        'predictions': predictions,
        'total_predictions': total_predictions,
        'title': 'My Profile',
    }
    return render(request, 'users/profile.html', context)
