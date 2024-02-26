from django.shortcuts import render



# Create your views here.
def index_home_section(request):
    return render(request, 'Home/index.html')