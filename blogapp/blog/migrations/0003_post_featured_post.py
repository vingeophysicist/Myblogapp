# Generated by Django 3.1.7 on 2021-03-08 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210308_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured_post',
            field=models.BooleanField(default=False),
        ),
    ]
