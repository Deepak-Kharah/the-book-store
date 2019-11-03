from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=50)


class Book(models.Model):
    image = models.ImageField(upload_to="media/", null=True)
    name = models.CharField(max_length=50)
    description = models.ManyToManyField(Genre)
