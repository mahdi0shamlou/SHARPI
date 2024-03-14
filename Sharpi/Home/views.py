from django.shortcuts import render
from .models import Tokens_alredy_have, Aparteman_buy_details


# Create your views here.
def index_home_section(request):
    my_list = Tokens_alredy_have.objects.all().values()
    my_list1 = Aparteman_buy_details.objects.all().values()
    print(my_list)
    print(my_list1)
    data_send_to_html = {'Apartments' : my_list1}
    return render(request, 'index.html', data_send_to_html)