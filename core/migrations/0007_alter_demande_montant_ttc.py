# Generated by Django 3.2 on 2021-04-15 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210415_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='montant_ttc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9999, null=True),
        ),
    ]
