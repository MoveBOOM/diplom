# Generated by Django 5.0.7 on 2024-07-28 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_parameter_alter_category_shops_contact_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'CREATED'), ('DONE', 'DONE')], default='CREATED', max_length=128),
        ),
    ]
