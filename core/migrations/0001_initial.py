# Generated by Django 4.2.10 on 2025-03-26 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plante',
            fields=[
                ('plante_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('moisture_max', models.BigIntegerField()),
                ('moisture_min', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True)),
                ('firstname', models.TextField()),
                ('lastname', models.TextField()),
                ('username', models.TextField()),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlante',
            fields=[
                ('users_plantes_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('plante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.plante')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
    ]
