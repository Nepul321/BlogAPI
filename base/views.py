from django.shortcuts import render

def HomeView(request):
    template = "base/home.html"
    context = {

    }

    return render(request, template, context)
