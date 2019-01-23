from django.db import models

# Create your models here.


class Owner(models.Model):
    """Owner model"""

    name = models.CharField(
        'Name', max_length=50, null=False, blank=False
    )

    def __str__(self):
        return self.name.replace(' ', '_')


class Company(models.Model):
    """Company model"""
    name = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Name'
    )

    owners = models.ManyToManyField(Owner, through='Relation')

    def __str__(self):
        return self.name


class Relation(models.Model):
    """Relation model"""
    position = models.CharField(
        'Position', max_length=50, null=False, blank=False
    )
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.position


class Trade(models.Model):
    """Insider trade model"""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name='Company'
    )

    insider = models.ForeignKey(
        Owner, blank=False, null=False, on_delete=models.CASCADE
    )

    last_date = models.DateField('LastDate', blank=False, null=False)

    transaction_type = models.CharField(
        'OwnerType', max_length=50, null=False, blank=False
    )

    owner_type = models.CharField(
        'OwnerType', max_length=20, null=False, blank=False
    )

    shares_traded = models.IntegerField('SharesTraded')
    last_price = models.DecimalField(
        'LastPrice', null=True, max_digits=10, decimal_places=2
    )
    shares_held = models.IntegerField('SharesHeld')

    @property
    def relation(self):
        return Relation.objects.get(
            company=self.company, owner=self.insider
        ).position


class StockPrice(models.Model):
    """StockPrice model"""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name='Company'
    )

    date = models.DateField('Date', blank=False, null=False)

    open = models.DecimalField('Open', max_digits=10, decimal_places=2)

    high = models.DecimalField('High', max_digits=10, decimal_places=2)

    low = models.DecimalField('Low', max_digits=10, decimal_places=2)

    close = models.DecimalField(
        'Close/Last', max_digits=10, decimal_places=2
    )

    volume = models.IntegerField('Volume')

    def __str__(self):
        return self.date
