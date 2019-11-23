from django.db import models

#TODO select correct models
class Model1(models.Model):
    pass
    # mts_id = models.CharField(max_length=256)
    # name = models.CharField(max_length=256)
    # country = models.CharField(max_length=256)
    # street = models.CharField(max_length=256)
    # brand = models.CharField(max_length=256)
    # plz = models.CharField(max_length=256)
    # lon = models.DecimalField(max_digits=15, decimal_places=11)
    # lat = models.DecimalField(max_digits=15, decimal_places=11)

    # def __str__(self) -> str:
    #     return self.name


class Model2(models.Model):
    pass
    # Fueltype and station together are unique
    # price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    # fueltype = models.CharField(max_length=256)
    # station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='prices')

    # def __str__(self) -> str:
    #     return str(self.price)
