# Generated by Django 2.2 on 2019-04-25 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0006_auto_20190423_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartItemData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('open', models.IntegerField()),
                ('close', models.IntegerField()),
                ('high', models.IntegerField()),
                ('low', models.IntegerField()),
                ('volume', models.IntegerField()),
            ],
        ),
    ]
