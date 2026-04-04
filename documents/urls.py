from django.urls import path
from documents.views import upload_document_view

urlpatterns = [
    path('upload/', upload_document_view, name='upload_document'),
]