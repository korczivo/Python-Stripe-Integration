# Generated by Django 3.2.5 on 2022-01-30 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_ex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='customer_id',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
    ]
