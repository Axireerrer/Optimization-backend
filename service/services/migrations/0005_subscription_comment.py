# Generated by Django 5.0.6 on 2024-05-21 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_plan_discount_percent_alter_plan_plan_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='comment',
            field=models.CharField(default='', max_length=40),
        ),
    ]