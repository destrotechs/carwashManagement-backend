from django.db import models
from services.models import Service
from users.models import User
from django.db.models import Sum
from customers.models import Customer

class Invoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,blank=True, null=True)
    sales = models.ManyToManyField("Sale", related_name="invoices")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)
    date_issued = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the invoice is new

        super().save(*args, **kwargs)  # Save first to get an ID

        if is_new:
            self.invoice_number = f"INV-{self.id:06d}"
            self.save(update_fields=["invoice_number"])  # Save only invoice_number field
    def update_payment_status(self):
        total_paid = self.payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.00
        self.total_paid = total_paid
        self.status = "paid" if total_paid >= self.total_amount else "pending"
        self.save(update_fields=["total_paid", "status"])

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.name if self.customer else ''}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments",blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.update_payment_status()

    def __str__(self):
        return f"Payment {self.id} - {self.amount_paid} via {self.payment_method}"

class Sale(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    employee = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_invoice")

    def __str__(self):
        return f"{self.service.name} - {self.customer.name if self.customer else 'No Customer'} - {self.amount}"
