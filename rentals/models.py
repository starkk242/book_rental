# rentals/models.py
from django.contrib.auth.models import User
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    number_of_pages = models.IntegerField()

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def calculate_fee(self):
        if self.end_date:
            rental_duration = (self.end_date - self.start_date).days
            
            # Calculate the number of months beyond the initial 30 days
            if rental_duration > 30:
                additional_days = rental_duration - 30
                additional_months = additional_days // 30
                fee = additional_months * (self.book.number_of_pages / 100)
                return fee
        return 0

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
