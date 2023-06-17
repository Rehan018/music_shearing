from django import forms
from .models import MusicFile


class MusicUploadForm(forms.ModelForm):
    class Meta:
        model = MusicFile
        fields = ['title', 'file', 'access']


class ProtectedMusicForm(forms.ModelForm):
    allowed_emails = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MusicFile
        fields = ['title', 'file', 'access']
