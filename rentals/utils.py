# rentals/utils.py
import requests

def fetch_book_details(title):
    response = requests.get(f'https://openlibrary.org/search.json?title={title}')
    if response.status_code == 200:
        data = response.json()
        if data['docs']:
            book_data = data['docs'][0]
            return {
                'title': book_data.get('title'),
                'author': book_data.get('author_name', ['Unknown'])[0],
                'number_of_pages': book_data.get('number_of_pages_median', 0)
            }
    return None
