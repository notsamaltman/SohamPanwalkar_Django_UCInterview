from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page),
    path('search/<str:searchtag>/', views.get_search)
]