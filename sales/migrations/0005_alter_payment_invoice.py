# Generated by Django 4.2.18 on 2025-02-09 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_invoice_payment_sale_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='sales.invoice'),
        ),
    ]
