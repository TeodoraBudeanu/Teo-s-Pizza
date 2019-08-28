from django.db import models
from django.urls import reverse


class Pizza(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    img_url = models.CharField(max_length=50, default="bg1.jpg")
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("details", args=[self.id])
