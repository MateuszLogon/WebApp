from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
