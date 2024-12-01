from django.shortcuts import render

def movies_list(request):
    return render(request, 'movies_list.html')
