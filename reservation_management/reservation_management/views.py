from django.shortcuts import render

def manifest_view(request):
    return render(request, 'manifest.json')