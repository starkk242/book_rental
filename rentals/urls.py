from django.urls import path
from . import views

urlpatterns = [
    path('start_rental/', views.start_rental, name='start_rental'),
    path('extend_rental/<int:rental_id>/', views.extend_rental, name='extend_rental'),
    path('rental_detail/<int:rental_id>/', views.rental_detail, name='rental_detail'),
    path('student_rentals/<int:user_id>/', views.student_rentals, name='student_rentals'),
    path('register/', views.register, name='register'),
    path('rental_success/', views.rental_success, name='rental_success'),
]
