from django.core.management.base import BaseCommand
from ...models import Book, Author, Category, Review
from django.contrib.auth.models import User
import random
from datetime import date

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    Category.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    Review.objects.all().delete()


def create_category():
    """Creates an address object combining different elements from the list"""
    category_names = ["Horror", "Romance", "Fantasy", "Children", "Folklore", "Historical", "Science", "Documentary"]
    for i in category_names:
        category = Category(
            name=i,
        )
        category.save()

def create_Author():
    """Creates an address object combining different elements from the list"""
    author_names = ["Stephen King", "J.K. Rowling", "J.R.R. Tolkien", "Roald Dahl", "Hans Christian Andersen", "George R.", "Isaac Asimov", "Carl Sagan", "Neil deGrasse Tyson", "Bill Nye",
                    "Stephen Hawking", "Richard Dawkins"]

    for i in author_names:
        author = Author(
            name=i,
        )
        author.save()

def create_book():
    """Creates an address object combining different elements from the list"""
    book_names = ["The Shining", "Harry Potter", "The Hobbit", "Charlie and the Chocolate Factory", "The Little Mermaid", "A Game of Thrones", "Foundation", "Cosmos", "Astrophysics for People in a Hurry", "Bill Nye's Big Ideas",
                  "A Brief History of Time", "The God Delusion", "Doraemon", "Shin cau be but chi", "Chu be nhut nhat", "The Little Prince", "A pewpew","Aloha"]

    for i in book_names:
        book = Book(
            title=i,
            price = random.randint(1, 100),
            author = random.choice(Author.objects.all()),
            category = random.choice(Category.objects.all()),
            quantity = random.randint(1, 100),
            #publish date date time
            published_date = date.today(),
        )
        book.save()

def create_review():
    reviews=["Good book", "Bad book", "Nice book", "Interesting book", "Boring book", "Waste of time", "Waste of money", "Waste of life"]
    for i in range(20):
        review = Review(
            review = random.choice(reviews),
            book = random.choice(Book.objects.all()),
            #user = random.choice(User.objects.all()),
            rating = random.randint(1, 5),
        )
        review.save()

# def Order():
#     order = Order(
#         #user = random.choice(User.objects.all()),
#         book = random.choice(Book.objects.all()),
#         quantity = random.randint(1, 100),
#         total_price = random.randint(1, 100),
#         order_date = date.today(),
#     )
#     order.save()

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    if mode == MODE_CLEAR:
        clear_data()
        self.stdout.write('data cleared.')
        return
    if mode == MODE_REFRESH:
        clear_data()
        self.stdout.write('data cleared.')
        
    create_category()
    create_Author()
    create_book()
    create_review()
    #Order()
    