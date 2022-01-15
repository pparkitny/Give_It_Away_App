from django.db import models

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
