# Generated by Django 4.2 on 2023-06-12 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_reviews', '0003_rename_imagen_url_autor_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comentario',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='valoracion',
            field=models.IntegerField(null=True),
        ),
    ]
