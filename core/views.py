from django.shortcuts import render
from documents.models import Document
from search_engine.models import SearchQuery
from automation.models import AutomationJob, SystemLog

# Create your views here.
def home_view(request):
    context = {
        'title': 'InsightForge',
        'status': 'Dashboard Placeholder active'
    }
    return render(request, 'core/home.html', context)

def dashboard_view(request):
    context = {
        'title': 'Dashboard',
        'documents': Document.objects.filter(owner=request.user).count(),
        'searches': SearchQuery.objects.filter(user=request.user).count(),
        'jobs': AutomationJob.objects.filter(owner=request.user).count(),
        'logs': SystemLog.objects.count(),
        'recent_documents': Document.objects.order_by('-updated_at')[:5]
    }

    return render(request, 'core/dashboard.html', context)