'''
This is a capstone project Models.py

'''
from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `
class CarMake(models.Model):
    '''Car Make Model
    '''
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
def __str__(self):
        return self.name 

class CarModel(models.Model):
    '''Car Model
    '''
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]

    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE, verbose_name='Select CarMake')
    dealerid = models.IntegerField()
    car_model_name = models.CharField(max_length=30)
    car_model_type = models.CharField(null=False, max_length=30,choices=TYPE_CHOICES,default=SEDAN)
    year = models.IntegerField()

    def __str__(self):
        return "Model: " + self.car_model_name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    '''Car Dealer Model
    '''
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    '''Car DealerReview Model
    '''
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make,car_model, car_year,id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.short_name = ""
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = ""
        self.id = id

    def __str__(self):
        return "Review: " + self.name
