# Generated by Django 4.2.1 on 2023-06-19 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppapp', '0003_alter_category_options_alter_product_index_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
