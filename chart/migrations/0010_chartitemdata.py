# Generated by Django 2.2 on 2019-04-25 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0009_delete_chartitemrawdata'),
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
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.ChartTicker')),
            ],
        ),
    ]
