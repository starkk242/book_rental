from datetime import timedelta
from django.test import TestCase
from .models import Book, Rental
from django.contrib.auth.models import User
from django.urls import reverse


class RentalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.book = Book.objects.create(title='Test Book', author='Author', number_of_pages=300)
        self.rental = Rental.objects.create(user=self.user, book=self.book)

    def test_calculate_fee(self):
        self.rental.end_date = self.rental.start_date + timedelta(days=60)
        self.assertEqual(self.rental.calculate_fee(), 3.0)

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', password='12345')

        # Create some test books
        self.book1 = Book.objects.create(title='Book 1', author='Author 1', number_of_pages=100)
        self.book2 = Book.objects.create(title='Book 2', author='Author 2', number_of_pages=150)

        # Create some test rentals
        self.rental1 = Rental.objects.create(user=self.test_user, book=self.book1)
        self.rental2 = Rental.objects.create(user=self.test_user, book=self.book2)

    def test_start_rental(self):
        # Test start rental view
        response = self.client.post(reverse('start_rental'), {'title': 'Book 1', 'user_id': self.test_user.id})
        self.assertEqual(response.status_code, 302)  # Check if redirected after successful rental

    def test_extend_rental(self):
        # Test extend rental view
        response = self.client.post(reverse('extend_rental', args=(self.rental1.id,)), {'end_date': '2024-06-01'})
        self.assertEqual(response.status_code, 302)  # Check if redirected after extending rental

    def test_rental_detail(self):
        # Test rental detail view
        response = self.client.get(reverse('rental_detail', args=(self.rental1.id,)))
        self.assertEqual(response.status_code, 302)  # Check if page loads successfully

    def test_student_rentals(self):
        # Test student rentals view
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('student_rentals'))
        self.assertEqual(response.status_code, 200)  # Check if page loads successfully
