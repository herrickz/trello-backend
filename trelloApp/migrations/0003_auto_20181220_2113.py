# Generated by Django 2.0.3 on 2018-12-20 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trelloApp', '0002_auto_20181204_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together={('trelloList', 'order')},
        ),
    ]