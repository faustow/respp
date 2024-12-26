from django.db import models


class Property(models.Model):
    id = models.UUIDField(primary_key=True, help_text="Unique identifier for the property")
    pid = models.IntegerField(help_text="Parcel Identification Number")
    lotarea = models.IntegerField(help_text="Lot size in square feet")
    overallqual = models.IntegerField(help_text="Overall material and finish quality")
    overallcond = models.IntegerField(help_text="Overall condition rating")
    centralair = models.BooleanField(help_text="Central air conditioning (True/False)")
    fullbath = models.IntegerField(help_text="Full bathrooms above grade")
    bedroomabvgr = models.IntegerField(help_text="Number of bedrooms above basement level")
    garagecars = models.IntegerField(null=True, blank=True, help_text="Size of garage in car capacity")
    saleprice = models.IntegerField(help_text="Sale price (in USD)")
    data_source = models.IntegerField(blank=False, null=False, default=1, help_text="1=Ames, 2=User provided")
    dataset = models.CharField(
        max_length=10,
        choices=[("training", "Training"), ("validation", "Validation"), ("test", "Test")],
        default="training",
    )

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return f"Property Pid{self.pid} - Price: {self.saleprice} (source={self.data_source},dataset={self.dataset})"
