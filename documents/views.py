from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import DocumentUploadForm
from .services import DocumentParser
from .models import Document, DocumentProcessingResult

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

            DocumentParser.parse_document(document)
            return redirect('upload_document')
    else:
        form = DocumentUploadForm()

    context = {
        'form': form
    }
    return render(request, 'documents/upload.html', context)

@login_required
def document_list_view(request):
    context = {
        'user_documents': Document.objects.filter(owner=request.user)
    }

    return render(request, 'documents/list.html', context)

@login_required
def document_detail_view(request, document_id):
    try:
        document = get_object_or_404(Document, id=document_id, owner=request.user)
        process_result = DocumentProcessingResult.objects.filter(document=document).first()
    except Http404:
        return render(request, 'error.html', {'msg': 'The document does not exist in the system'})

    context = {
        'document': document,
        'process_result': process_result
    }

    return render(request, 'documents/detail.html', context)