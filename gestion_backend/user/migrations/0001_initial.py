# Generated by Django 4.2.3 on 2023-08-08 01:02

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='El nombre debe contener solo letras.', regex='^[a-zA-Z]+$')])),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='El nombre debe contener solo letras.', regex='^[a-zA-Z]+$')])),
                ('email_address', models.EmailField(error_messages={'unique': 'Correo electrónico en uso.'}, max_length=254, unique=True)),
                ('phone', models.CharField(error_messages={'unique': 'Número de teléfono ya registrado.'}, max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe tener un formato válido', regex='^(\\+?54|0)(\\d{10}|\\d{2,4}\\s?\\d{6,10})$')])),
                ('password', models.CharField(max_length=32)),
                ('failed_login_attempts', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('register_code', models.CharField(blank=True, max_length=6, null=True)),
                ('register_code_created_at', models.DateTimeField(blank=True, null=True)),
                ('reset_password_token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('reset_password_token_created_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]