from django.db import models
from django.urls import reverse


class Pizza(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/', null=True)
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("details", args=[self.id])
