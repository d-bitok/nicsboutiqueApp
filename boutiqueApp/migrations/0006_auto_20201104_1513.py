# Generated by Django 3.1.3 on 2020-11-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutiqueApp', '0005_auto_20201104_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
