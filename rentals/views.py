# rentals/views.py
from django.shortcuts import render, redirect
from .models import Book, Rental
from .utils import fetch_book_details
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_rentals', user_id=user.id)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def start_rental(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user_id = request.POST.get('user_id')
        book_details = fetch_book_details(title)
        if book_details:
            book, created = Book.objects.get_or_create(
                title=book_details['title'],
                author=book_details['author'],
                number_of_pages=book_details['number_of_pages']
            )
            Rental.objects.create(user_id=user_id, book=book)
            return redirect('rental_success')
    return render(request, 'start_rental.html')

def extend_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.end_date = request.POST.get('end_date')
    rental.save()
    return redirect('rental_detail', rental_id=rental_id)

def rental_detail(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    fee = rental.calculate_fee()
    return render(request, 'rental_detail.html', {'rental': rental, 'fee': fee})

def student_rentals(request, user_id):
    rentals = Rental.objects.filter(user_id=user_id)
    return render(request, 'student_rentals.html', {'rentals': rentals})

def rental_success(request):
    return render(request, 'rental_success.html')