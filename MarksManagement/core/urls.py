from django.urls import path
from .views import register, user_login, user_logout, dashboard
from .views import marks_list, marks_create, marks_update, marks_delete, home, view_all_marks, view_my_marks,download_result

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('marks/', marks_list, name='marks_list'),
    path('marks/new/', marks_create, name='marks_create'),
    path('marks/edit/<int:pk>/', marks_update, name='marks_update'),
    path('marks/delete/<int:pk>/', marks_delete, name='marks_delete'),
    path('teacher/marks/', view_all_marks, name='view_all_marks'),
    path('student/marks/', view_my_marks, name='view_my_marks'),
    path('download-result/', download_result, name='download_result'),
]