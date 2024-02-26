from django.urls import path
from views import index_home_section

urlpatterns = [
    path('', index_home_section, name='Index_of_Home_section')

]