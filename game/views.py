from django.shortcuts import render


def index(request):
    context = {'message': "Welcome to the game"}
    return render(request, 'game/index.html', context)