# Generated by Django 4.2.2 on 2023-06-18 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0004_alter_product_options_remove_product_product_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='product',
            name='availability',
            field=models.BooleanField(default=True, verbose_name='Наявність'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='online_store.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис товару'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Назва товару'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(upload_to='photos/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='online_store.size', verbose_name='Розмір'),
        ),
    ]
