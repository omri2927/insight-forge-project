from django.urls import path
from .views import upload_document_view, document_list_view, document_detail_view

urlpatterns = [
    path('upload/', upload_document_view, name='upload_document'),
    path('list/', document_list_view, name='documents_list'),
    path('<int:document_id>/detail/', document_detail_view, name='document_detail')
]