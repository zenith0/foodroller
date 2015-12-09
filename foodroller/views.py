from django.shortcuts import render, render_to_response


def index(request):
    return render_to_response('index.html')


def categories(request):
    return render_to_response('categories.html')


def roll(request):
    return render_to_response('roll.html')
