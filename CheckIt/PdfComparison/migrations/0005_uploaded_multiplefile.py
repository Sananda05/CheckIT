# Generated by Django 3.2.4 on 2021-10-14 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PdfComparison', '0004_auto_20210920_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='uploaded_multipleFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='compare_multiple')),
                ('is_compared', models.BooleanField(default=False)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
