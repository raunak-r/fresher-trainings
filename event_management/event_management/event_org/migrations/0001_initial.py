# Generated by Django 4.2 on 2023-04-29 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=100, null=True)),
                ('phone', models.CharField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=100)),
                ('event_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('event_cost', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('Booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_booking', models.DateField(auto_now_add=True, null=True)),
                ('count', models.IntegerField(null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_org.customer')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_org.event')),
            ],
        ),
    ]
