from django.urls import path
from . import views

app_name = 'autos'  # Убедитесь, что эта строка есть!

urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    
    # ПУТИ ДЛЯ МАШИН (AUTOS)
    path('main/create/', views.AutoCreate.as_view(), name='auto_create'), # Должен быть ВЫШЕ <int:pk>
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='auto_update'),
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='auto_delete'),
    
    # ПУТИ ДЛЯ МАРОК (MAKES)
    path('lookup/', views.MakeView.as_view(), name='make_list'),
    path('lookup/create/', views.MakeCreate.as_view(), name='make_create'), # Должен быть ВЫШЕ <int:pk>
    path('lookup/<int:pk>/update/', views.MakeUpdate.as_view(), name='make_update'),
    path('lookup/<int:pk>/delete/', views.MakeDelete.as_view(), name='make_delete'),
]