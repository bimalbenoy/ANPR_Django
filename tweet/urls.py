

from django.urls import path
from .  import views







urlpatterns = [
    path('',views.tweet_list,name='tweet_list'),
    path('create/',views.tweet_create,name='tweet_create'),
    path('<int:tweet_id>/edit/',views.tweet_edit,name='tweet_edit'),
    path('<int:tweet_id>/delete/',views.tweet_delete,name='tweet_delete'),
    path('register/',views.register,name='register'),
    path('searched/',views.tweet_search,name='searched'),
    path('home1/',views.home1,name='home1'),
    path('logbook/',views.logbook,name='logbook'),
    path('upload/',views.upload,name='upload'),
    path('gateopen/',views.gateopen,name='gateopen'),
    path('gateclose/',views.gateclose,name='gateclose'),

]
