# Generated by Django 3.2 on 2022-05-04 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20220429_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.tag'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_image',
            field=models.ImageField(db_column='Store_image', max_length=255, upload_to=''),
        ),
    ]
