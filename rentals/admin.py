# rentals/admin.py
from django.contrib import admin
from .models import Book, Rental

admin.site.register(Book)
admin.site.register(Rental)
