# Generated by Django 4.2.16 on 2024-10-16 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='media/blog/', verbose_name='Изображение'),
        ),
    ]
