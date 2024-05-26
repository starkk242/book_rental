from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='root'),
    path('start_rental/', views.start_rental, name='start_rental'),
    path('student_rentals/', views.student_rentals, name='student_rentals'),
    path('register/', views.register, name='register'),
    path('add_user/', views.add_user, name='add_user'),
    path('rental_success/', views.rental_success, name='rental_success'),
    path('extend_rental/<int:rental_id>/', views.extend_rental, name='extend_rental'),
    path('report/', views.rental_report, name='rental_report'),
]