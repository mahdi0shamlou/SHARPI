from django.shortcuts import render
from .models import Tokens_alredy_have, Aparteman_buy_details


# Create your views here.
def index_home_section(request):
    limit = request.GET.get('limit')
    page = int(request.GET.get('page'))
    number_page_limit = (page*10)
    number_page_limit_past = number_page_limit - 10
    Aparteman_buy_details_list = Aparteman_buy_details.objects.all().values().order_by('-id')[number_page_limit_past:number_page_limit]
    Aparteman_buy_details_list_filterd = Aparteman_buy_details.objects.filter(mahal_persian='فردوسی').values()
    print(Aparteman_buy_details_list_filterd)
    data_send_to_html = {'Apartments' : Aparteman_buy_details_list,
                         'user': 'admin',
                         'path': 'home',
                         'email': 'admin@gmail.com',
                         'page' : page
                         }
    return render(request, 'Home/index.html', data_send_to_html)