# Generated by Django 4.0.4 on 2022-07-21 14:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homes', '0002_alter_home_options_alter_home_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_initial', models.CharField(max_length=1)),
                ('on_hiatus', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'resident',
                'verbose_name_plural': 'residents',
                'db_table': 'resident',
            },
        ),
        migrations.CreateModel(
            name='Residency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_in', models.DateField(default=django.utils.timezone.now)),
                ('move_out', models.DateField(blank=True, null=True)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='homes.home')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='residents.resident')),
            ],
            options={
                'verbose_name': 'residency',
                'verbose_name_plural': 'residencies',
                'db_table': 'residency',
            },
        ),
    ]
