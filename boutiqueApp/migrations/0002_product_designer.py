# Generated by Django 3.1.3 on 2020-11-09 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boutiqueApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='designer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
