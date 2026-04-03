from django.shortcuts import render

# Create your views here.
def home_view(request):
    context = {
        'title': 'InsightForge',
        'status': 'Dashboard Placeholder active'
    }
    return render(request, 'core/home.html', context)