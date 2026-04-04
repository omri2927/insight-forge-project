from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document

        fields = ['title', 'stored_file', 'document_type']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-4',
                'placeholder': 'Enter document title...',
            }),
            'stored_file': forms.FileInput(attrs={
                'class': 'form-control rounded-pill',
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-select rounded-pill px-4',
            }),
        }

        labels = {
            'title': 'Document Title',
            'stored_file': 'Select File',
            'document_type': 'Category',
        }