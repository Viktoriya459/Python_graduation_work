# Generated by Django 4.2.2 on 2023-06-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
