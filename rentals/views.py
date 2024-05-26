from collections import defaultdict
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm
from .models import Book, Rental
from .utils import fetch_book_details
from django.views.decorators.csrf import csrf_exempt


def admin_required(user):
    """Check if the user is a staff member."""
    return user.is_staff


def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_rentals', user_id=user.id)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    """Redirect to student rentals."""
    return redirect('student_rentals')


@user_passes_test(admin_required)
def start_rental(request):
    """Start a new rental."""
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

    users = User.objects.all()  # Fetch all users
    return render(request, 'start_rental.html', {'users': users})


@user_passes_test(admin_required)
def extend_rental(request, rental_id):
    """Extend the rental period."""
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == 'POST':
        new_end_date = request.POST.get('end_date')
        rental.end_date = new_end_date
        rental.save()
        return redirect('student_rentals')
    return render(request, 'extend_rental.html', {'rental': rental})


@login_required
def student_rentals(request):
    """View rentals for students."""
    user = request.user
    if user.is_staff:
        rentals = Rental.objects.all()
    else:
        rentals = Rental.objects.filter(user=user)

    # Group rentals by user
    grouped_rentals = defaultdict(list)
    for rental in rentals:
        grouped_rentals[rental.user].append(rental)

    return render(request, 'student_rentals.html', {'grouped_rentals': dict(grouped_rentals)})


def rental_success(request):
    """Display rental success message."""
    return render(request, 'rental_success.html')


@csrf_exempt
def add_user(request):
    """Add a new user."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'id': user.id, 'username': user.username})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def rental_report(request):
    """Generate rental report."""
    # Total rentals per book
    rentals_per_book = Rental.objects.values('book__title').annotate(total_rentals=Count('id'))

    # Total rentals per user
    rentals_per_user = Rental.objects.values('user__username').annotate(total_rentals=Count('id'))

    # Average rental duration
    rental_durations = Rental.objects.annotate(duration=F('end_date') - F('start_date'))
    average_rental_duration = rental_durations.aggregate(average_duration=Avg('duration'))

    # Most rented books
    most_rented_books = Rental.objects.values('book__title').annotate(total_rentals=Count('id')).order_by('-total_rentals')[:5]

    paginator = Paginator(rentals_per_book, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'rentals_per_book': page_obj,
        'rentals_per_user': rentals_per_user,
        'average_rental_duration': average_rental_duration['average_duration'],
        'most_rented_books': most_rented_books,
    }

    return render(request, 'rental_report.html', context)