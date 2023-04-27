from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('daohang/',views.dao_hang,name='daohang'),
    path('renwubangding/', views.renwu_record, name='renwubangding'),
    path('add_renwu/',views.add_renwu,name="addrenwu"),
    path('jiandui/',views.add_jiandui,name="dengji"),
    path('my_jiandui', views.my_chuqin, name='my_jiandui'),
    path('juntuan_scores/', views.juntuan_scores, name='juntuan_scores'),

]
