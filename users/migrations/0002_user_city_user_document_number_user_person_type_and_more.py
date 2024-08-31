# Generated by Django 5.1 on 2024-08-23 02:02

import django.db.models.deletion
import stdimage.models
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorys', '0002_alter_category_description'),
        ('cities', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cities.city', verbose_name='city'),
        ),
        migrations.AddField(
            model_name='user',
            name='document_number',
            field=models.CharField(max_length=14, null=True, verbose_name='document number'),
        ),
        migrations.AddField(
            model_name='user',
            name='person_type',
            field=models.CharField(choices=[('P', 'Person'), ('C', 'Company')], max_length=2, null=True, verbose_name='person type'),
        ),
        migrations.AlterField(
            model_name='user',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='categorys.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(max_length=120, null=True, verbose_name='full name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image_profile',
            field=stdimage.models.StdImageField(default=None, force_min_size=False, upload_to=users.models.get_file_path, variations={'thumb': {'crop': True, 'height': 512, 'width': 512}}, verbose_name='Image Profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated At'),
        ),
    ]
