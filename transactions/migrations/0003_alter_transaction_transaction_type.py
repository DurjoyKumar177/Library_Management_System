# Generated by Django 5.1 on 2024-11-22 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposite'), (2, 'Payment'), (3, 'Refund'), (4, 'Withdrawal')], null=True),
        ),
    ]
