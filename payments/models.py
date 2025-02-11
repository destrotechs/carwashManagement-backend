# from django.db import models
# from sales.models import Sale
#
# class Payment(models.Model):
#     PAYMENT_METHODS = [
#         ('cash', 'Cash'),
#         ('mpesa', 'M-Pesa'),
#         ('card', 'Card'),
#         ('bank_transfer', 'Bank Transfer'),
#     ]
#
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     date_paid = models.DateTimeField(auto_now_add=True)
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
#     transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
#     remarks = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f"Payment {self.id} - {self.amount_paid} via {self.payment_method}"
#
# class Sale_Payment(models.Model):
#     sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
