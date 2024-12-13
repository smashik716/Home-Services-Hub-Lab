# Generated by Django 3.2.6 on 2021-08-28 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0011_auto_20200709_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notesfile', models.FileField(null=True, upload_to='')),
                ('uploaddate', models.DateField(null=True)),
                ('serviceman', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home_service.service_man')),
            ],
        ),
    ]