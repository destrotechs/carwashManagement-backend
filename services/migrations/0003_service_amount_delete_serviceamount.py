# Generated by Django 4.2.18 on 2025-02-03 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_item_service_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.DeleteModel(
            name='ServiceAmount',
        ),
    ]
