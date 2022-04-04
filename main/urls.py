from django.urls import path
from .views import *
from .import views
urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<str:slug>/', views.category_detail, name ='category'),
    path('apt-detail/<int:pk>/', views.apt_detail, name='detail'),
    path('add-info/', views.add_info, name='add-info'),
    path('update-info/<int:pk>/', views.update_info, name='update-info'),
    path('delete-info/<int:pk>', views.DeleteRecipeView.as_view(), name='delete-info'),
]