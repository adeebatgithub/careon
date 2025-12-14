from django.db import models

class Products(models.Model):
    ATTACHED=1
    NOT_ATTACHED=0
    REINFORCEMENTS=(
        (ATTACHED, 'Attached'),
        (NOT_ATTACHED, 'Not Attached')
    )
    NORMAL_FOLDING=0
    AMRITHA_FOLDING=1
    FOLDS=(
        (NORMAL_FOLDING, 'Normal'),
        (AMRITHA_FOLDING, 'Amritha'),
    )
    name = models.CharField(max_length=100)
    reinforcement = models.PositiveSmallIntegerField(choices=REINFORCEMENTS)
    folding = models.PositiveSmallIntegerField(choices=FOLDS)
    default = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Orders(models.Model):
    name = models.CharField(max_length=100)

    def _get_products(self, **kwargs):
        return OrderProducts.objects.filter(order=self, **kwargs)

    def products(self):
        return self._get_products()

    def total_demand(self):
        return self._get_products().aggregate(models.Sum('demand'))['demand__sum'] or 0


class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    demand = models.PositiveIntegerField()
