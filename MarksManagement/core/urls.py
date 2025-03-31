from django.urls import path
from .views import register, user_login, user_logout, dashboard
from .views import marks_list, marks_create, marks_update, marks_delete

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('marks/', marks_list, name='marks_list'),
    path('marks/new/', marks_create, name='marks_create'),
    path('marks/edit/<int:pk>/', marks_update, name='marks_update'),
    path('marks/delete/<int:pk>/', marks_delete, name='marks_delete'),
]