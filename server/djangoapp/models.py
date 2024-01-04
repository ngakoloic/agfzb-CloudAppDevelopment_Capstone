from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=True, max_length=50)
    color = models.CharField(null=True, max_length=50)
    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    MODELS = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(default='')
    model_type = models.CharField(max_length=10, choices=MODELS, default=SEDAN)
    year = models.DateField()
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE, default='')
    def __str__(self):
        return self.name+ \
                ' for '+self.carmake.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
