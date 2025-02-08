from django.db import models
from services.models import Service
from users.models import User
class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    id_no = models.CharField(max_length=255,blank=True, null=True)

class Sale(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    employee = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service.name} - {self.customer_name} - {self.amount}"

