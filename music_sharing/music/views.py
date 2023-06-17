from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MusicUploadForm, ProtectedMusicForm
from .models import MusicFile, AllowedUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Q

def home(request):
    if request.user.is_authenticated:
        user = request.user
        music_files = MusicFile.objects.filter(
            Q(access='public') | Q(user=user) | Q(alloweduser__email=user.email)
        ).distinct()
        return render(request, 'music/home.html', {'music_files': music_files})
    else:
        return render(request, 'music/home.html')

@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            messages.success(request, 'Music file uploaded successfully.')
            return redirect('home')
    else:
        form = MusicUploadForm()
    return render(request, 'music/upload_music.html', {'form': form})

@login_required
def protected_music(request):
    if request.method == 'POST':
        form = ProtectedMusicForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            allowed_emails = form.cleaned_data['allowed_emails'].split(',')
            for email in allowed_emails:
                AllowedUser.objects.create(music_file=music_file, email=email.strip())
            messages.success(request, 'Protected music file uploaded successfully.')
            return redirect('home')
    else:
        form = ProtectedMusicForm()
    return render(request, 'music/protected_music.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'music/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'music/profile.html')

