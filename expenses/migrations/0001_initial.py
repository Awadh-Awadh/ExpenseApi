# Generated by Django 4.0.1 on 2022-01-19 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(choices=[('ONLINE', 'ONLINE'), ('TRAVE', 'TRAVEL'), ('EXECUTIVE', 'EXECUTIVE'), ('PREMIUM', 'PREMIUM'), ('BASIC', 'BASIC'), ('MIDDLE', 'MIDDLE')], max_length=255)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=5)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
