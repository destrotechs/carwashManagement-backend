from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps  # Delayed model import
from sales.models import Sale

@receiver(post_save, sender=Sale)
def create_or_update_commission(sender, instance, **kwargs):
    """Create or update an employee's commission when a sale is saved."""
    SaleCommission = apps.get_model("commissions", "SaleCommission")
    CommissionSetting = apps.get_model("commissions", "CommissionSetting")

    if instance.employee:
        commission_setting = CommissionSetting.objects.filter(
            employee=instance.employee, service=instance.service
        ).first()

        commission_amount = (
            (commission_setting.percentage / 100) * instance.amount if commission_setting else 0
        )

        SaleCommission.objects.update_or_create(
            sale=instance,
            defaults={"employee": instance.employee, "commission_amount": commission_amount}  # Add employee
        )

@receiver(post_delete, sender=Sale)
def delete_commission(sender, instance, **kwargs):
    """Delete commission when a sale is deleted."""
    SaleCommission = apps.get_model("commissions", "SaleCommission")
    SaleCommission.objects.filter(sale=instance).delete()
