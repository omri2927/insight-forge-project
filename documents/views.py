from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm

# Create your views here.
@login_required
def upload_document_view(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user

            uploaded_file = request.FILES['stored_file']
            document.original_file_name = uploaded_file.name
            document.file_size = uploaded_file.size
            document.save()
            return redirect('upload_document')
    else:
        form = DocumentUploadForm()

    context = {
        'form': form
    }
    return render(request, 'documents/upload.html', context)