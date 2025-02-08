from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(Item, related_name="services")  # A service can belong to multiple items
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # A service may have a different price per item
    def __str__(self):
        return self.name


