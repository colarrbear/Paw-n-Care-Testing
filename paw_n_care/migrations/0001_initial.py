# Generated by Django 5.1 on 2024-11-22 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('reason', models.TextField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=255)),
                ('registration_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Veterinarian',
            fields=[
                ('vet_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('specialization', models.CharField(max_length=255)),
                ('license_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(max_length=20)),
                ('payment_method', models.CharField(max_length=20)),
                ('payment_date', models.DateTimeField()),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing', to='paw_n_care.appointment')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='paw_n_care.owner'),
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('pet_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('species', models.CharField(max_length=50)),
                ('breed', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='paw_n_care.owner')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='paw_n_care.pet'),
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('visit_date', models.DateTimeField()),
                ('diagnosis', models.TextField()),
                ('treatment', models.TextField()),
                ('prescribed_medication', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='paw_n_care.pet')),
                ('vet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='paw_n_care.veterinarian')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='vet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='paw_n_care.veterinarian'),
        ),
    ]
