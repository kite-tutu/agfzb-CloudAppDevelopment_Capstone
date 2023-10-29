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
class CarDealer(models.Model):
    '''Car Dealer Model
    '''
    dealerid = models.IntegerField()
    dealer_firstname = models.CharField(max_length=30)
    dealer_lastname = models.CharField(max_length=30)
    dealer_email = models.EmailField(max_length=20)
    dealer_phoneno = models.CharField(max_length=30)

    def __str__(self):
        return "Names: " + self.dealer_firstname + " " + \
                self.dealer_lastname

class DealerReview(models.Model):
    ''' Dealer Review Model
    '''
    dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    review_id = models.CharField(max_length=30)

    def __str__(self):
        return self.dealer + " " + self.review_id
