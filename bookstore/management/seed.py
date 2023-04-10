from django.core.management.base import BaseCommand
from ..models import Book, Author, Category, Review
import random

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


def create_category(index):
    category_names = ["Horror", ]

    category = Category(
        name=category_names[index],
    )
    category.save()
    return category

def create_category():
    """Creates an address object combining different elements from the list"""
    street_flats = ["#221 B", "#101 A", "#550I", "#420G", "#A13"]
    street_localities = ["Bakers Street", "Rajori Gardens", "Park Street", "MG Road", "Indiranagar"]
    pincodes = ["101234", "101232", "101231", "101236", "101239"]
    category_names = ["Horror", "Romance", "Fantasy", "Children", "Folklore", "Historical", "Science", "Documentary", ""]

    address = Category(
        name=random.choice(category_names),
    )
    address.save()
    return address

def create_category():
    """Creates an address object combining different elements from the list"""
    street_flats = ["#221 B", "#101 A", "#550I", "#420G", "#A13"]
    street_localities = ["Bakers Street", "Rajori Gardens", "Park Street", "MG Road", "Indiranagar"]
    pincodes = ["101234", "101232", "101231", "101236", "101239"]
    category_names = ["Horror", ]

    address = Category(
        name=random.choice(category_names),
    )
    address.save()
    return address

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    for i in range(10):
        create_category(i)

    for i in range(25):
        create_author()
        create_book()
        
    for i in range(15):
        create_review()