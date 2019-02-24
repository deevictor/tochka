# Generated by Django 2.1.5 on 2019-02-24 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50, verbose_name='Position')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.Company')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('open', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Open')),
                ('high', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='High')),
                ('low', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Low')),
                ('close', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Close/Last')),
                ('volume', models.IntegerField(verbose_name='Volume')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.Company', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_date', models.DateField(verbose_name='LastDate')),
                ('transaction_type', models.CharField(max_length=50, verbose_name='OwnerType')),
                ('owner_type', models.CharField(max_length=20, verbose_name='OwnerType')),
                ('shares_traded', models.IntegerField(verbose_name='SharesTraded')),
                ('last_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='LastPrice')),
                ('shares_held', models.IntegerField(verbose_name='SharesHeld')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.Company', verbose_name='Company')),
                ('insider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.Owner')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='owners',
            field=models.ManyToManyField(through='trades.Relation', to='trades.Owner'),
        ),
    ]