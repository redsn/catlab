from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('cat_detail', kwargs={'cat_id': self.id })


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
        )
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    ## self.get_meal_display()
    def __str__(self):
        return f'{self.get_meal_display()} for {self.cat.name} on {self.date}'
    class Meta:
        ordering = ['-date']

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return f'A(n) {self.color} {self.name}'
    class Meta:
        ordering = ['-color']

    def get_absolute_url(self):
        return reverse('toy_detail', kwargs={'toy_id': self.id})