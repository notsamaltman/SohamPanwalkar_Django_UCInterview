from django.db import models

# Create your models here.
class Drink(models.Model):
    name = models.TextField(max_length=200, primary_key=True)
    image = models.TextField(default='')
    searches = models.IntegerField(default=0)

    def __str__(self):
        return self.name