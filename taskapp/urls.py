from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page),
    path('search/<str:searchtag>/', views.get_search),
    path('home/<str:drinkName>/', views.info_page),
    path('mostsearched/', views.top10page),
]