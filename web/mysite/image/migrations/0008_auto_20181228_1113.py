# Generated by Django 2.1.1 on 2018-12-28 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0007_auto_20181228_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]