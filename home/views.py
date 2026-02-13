from django.shortcuts import render
def home_inicio(request):
    return render(request, 'home/home.html', {})
