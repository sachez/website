from django.urls import path
from django.contrib.auth.views import logout, login
from payments.views import (register, user_home, sign_in, take_credit, verification,
                            check_reg_form, ajax_check_form, get_curse)

urlpatterns = [
    path('register/', register, name='register'),
    path('sign_in/', sign_in, name='sign_in'),
    path('login/', login),
    path('logout/', logout,
         {
             'next_page': '/payments/sign_in'
         },
         name='logout'),
    path('user=<int:id>/', user_home, name='user_home'),
    path('take_credit/', take_credit, name='take_credit'),
    path('verification/', verification, name='verification'),
    path('ajax/check_reg_form/', ajax_check_form, name='check_reg_form'),
    path('ajax/get_curse/',
         get_curse, name='get_curse'),
]
