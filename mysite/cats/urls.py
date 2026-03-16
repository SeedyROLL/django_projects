from django.urls import path
from . import views

# Обязательно для разделения пространств имен (cats:all vs autos:all)
app_name = 'cats'

urlpatterns = [
    # Список всех кошек
    path('', views.CatList.as_view(), name='all'),
    
    # Операции с кошками (Main)
    # Путь 'create' должен быть ВЫШЕ путей с <int:pk>
    path('main/create/', views.CatCreate.as_view(), name='cat_create'),
    path('main/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
    path('main/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
    
    # Операции с породами (Lookup)
    path('lookup/', views.BreedList.as_view(), name='breed_list'),
    path('lookup/create/', views.BreedCreate.as_view(), name='breed_create'),
    path('lookup/<int:pk>/update/', views.BreedUpdate.as_view(), name='breed_update'),
    path('lookup/<int:pk>/delete/', views.BreedDelete.as_view(), name='breed_delete'),
]