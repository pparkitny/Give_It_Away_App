from django.db import models
from django.contrib.auth.models import User

TYPES_OF_INSTITUTION = (
    (1, "Fundacja"),
    (2, "Organizacja pozarządowa"),
    (3, "Zbiórka lokalna")
)


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    type = models.IntegerField(choices=TYPES_OF_INSTITUTION)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution,  on_delete=models.CASCADE)
    address = models.CharField(max_length=124)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateTimeField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
