from django.db import models

from users.models import User
from sales.models import Sale, Service

class CommissionSetting(models.Model):
    """Defines different commission percentages per service per employee."""
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.employee.username} - {self.service.name} - {self.percentage}%"

class SaleCommission(models.Model):
    """Tracks commission payments for a sale."""
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this field
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(null=True, blank=True)

    def calculate_commission(self):
        """Calculates commission dynamically based on the employee and service."""
        if not self.sale.employee:
            return 0

        try:
            commission_setting = CommissionSetting.objects.get(
                employee=self.sale.employee, service=self.sale.service
            )
            return (commission_setting.percentage / 100) * self.sale.amount
        except CommissionSetting.DoesNotExist:
            return 0  # No commission if no setting exists

    def save(self, *args, **kwargs):
        """Auto-calculate commission before saving."""
        if self.commission_amount is None:
            self.commission_amount = self.calculate_commission()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Paid" if self.paid else "Unpaid"
        return f"{self.sale} - {self.commission_amount} ({status})"

