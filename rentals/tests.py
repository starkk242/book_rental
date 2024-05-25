# rentals/tests.py
from django.test import TestCase
from .models import Book, Rental
from django.contrib.auth.models import User

class RentalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.book = Book.objects.create(title='Test Book', author='Author', number_of_pages=300)
        self.rental = Rental.objects.create(user=self.user, book=self.book)

    def test_calculate_fee(self):
        self.rental.end_date = self.rental.start_date + timedelta(days=60)
        self.assertEqual(self.rental.calculate_fee(), 30 * (self.book.number_of_pages / 100))
