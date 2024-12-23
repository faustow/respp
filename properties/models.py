from django.db import models


class Property(models.Model):
    # Identifying and general information
    id = models.UUIDField(primary_key=True, help_text="Unique identifier for the property")
    pid = models.IntegerField(help_text="Parcel Identification Number")
    mssubclass = models.IntegerField(help_text="The building class")
    mszoning = models.CharField(max_length=50, help_text="General zoning classification")
    lotfrontage = models.FloatField(null=True, blank=True, help_text="Linear feet of street connected to property")
    lotarea = models.IntegerField(help_text="Lot size in square feet")
    street = models.CharField(max_length=50, help_text="Type of road access")
    alley = models.CharField(max_length=50, null=True, blank=True, help_text="Type of alley access")
    lotshape = models.CharField(max_length=50, help_text="General shape of property")
    landcontour = models.CharField(max_length=50, help_text="Flatness of the property")
    utilities = models.CharField(max_length=50, help_text="Type of utilities available")
    lotconfig = models.CharField(max_length=50, help_text="Lot configuration")
    landslope = models.CharField(max_length=50, help_text="Slope of property")
    neighborhood = models.CharField(max_length=50, help_text="Physical location within Ames")
    condition1 = models.CharField(max_length=50, help_text="Proximity to main road or railroad")
    condition2 = models.CharField(max_length=50, help_text="Proximity to main road or railroad (if a second exists)")
    bldgtype = models.CharField(max_length=50, help_text="Type of dwelling")
    housestyle = models.CharField(max_length=50, help_text="Style of dwelling")
    overallqual = models.IntegerField(help_text="Overall material and finish quality")
    overallcond = models.IntegerField(help_text="Overall condition rating")
    yearbuilt = models.IntegerField(help_text="Original construction date")
    yearremodadd = models.IntegerField(help_text="Remodel date (if applicable)")
    roofstyle = models.CharField(max_length=50, help_text="Type of roof")
    roofmatl = models.CharField(max_length=50, help_text="Roof material")
    exterior1st = models.CharField(max_length=50, help_text="Exterior covering on house")
    exterior2nd = models.CharField(max_length=50, help_text="Exterior covering on house (if more than one)")
    masvnrtype = models.CharField(max_length=50, null=True, blank=True, help_text="Masonry veneer type")
    masvnrarea = models.FloatField(null=True, blank=True, help_text="Masonry veneer area in square feet")
    exterqual = models.CharField(max_length=50, help_text="Quality of exterior material")
    extercond = models.CharField(max_length=50, help_text="Condition of exterior material")
    foundation = models.CharField(max_length=50, help_text="Type of foundation")
    bsmtqual = models.CharField(max_length=50, null=True, blank=True, help_text="Height of the basement")
    bsmtcond = models.CharField(max_length=50, null=True, blank=True, help_text="General condition of the basement")
    bsmtexposure = models.CharField(max_length=50, null=True, blank=True,
                                    help_text="Walkout or garden level basement walls exposure")
    bsmtfintype1 = models.CharField(max_length=50, null=True, blank=True, help_text="Finished basement area type 1")
    bsmtfinsf1 = models.IntegerField(null=True, blank=True, help_text="Type 1 finished square feet")
    bsmtfintype2 = models.CharField(max_length=50, null=True, blank=True, help_text="Finished basement area type 2")
    bsmtfinsf2 = models.IntegerField(null=True, blank=True, help_text="Type 2 finished square feet")
    bsmtunfsf = models.IntegerField(null=True, blank=True, help_text="Unfinished square feet of basement area")
    totalbsmtsf = models.IntegerField(null=True, blank=True, help_text="Total square feet of basement area")
    heating = models.CharField(max_length=50, help_text="Type of heating")
    heatingqc = models.CharField(max_length=50, help_text="Heating quality and condition")
    centralair = models.CharField(max_length=1, help_text="Central air conditioning (Y/N)")
    electrical = models.CharField(max_length=50, null=True, blank=True, help_text="Electrical system")
    firstflrsf = models.IntegerField(help_text="First floor square feet")
    secondflrsf = models.IntegerField(help_text="Second floor square feet")
    lowqualfinsf = models.IntegerField(help_text="Low quality finished square feet (all floors)")
    grlivarea = models.IntegerField(help_text="Above grade (ground) living area square feet")
    bsmtfullbath = models.IntegerField(null=True, blank=True, help_text="Basement full bathrooms")
    bsmthalfbath = models.IntegerField(null=True, blank=True, help_text="Basement half bathrooms")
    fullbath = models.IntegerField(help_text="Full bathrooms above grade")
    halfbath = models.IntegerField(help_text="Half baths above grade")
    bedroomabvgr = models.IntegerField(help_text="Number of bedrooms above basement level")
    kitchenabvgr = models.IntegerField(help_text="Number of kitchens")
    kitchenqual = models.CharField(max_length=50, help_text="Kitchen quality")
    totrmsabvgrd = models.IntegerField(help_text="Total rooms above grade (excluding bathrooms)")
    functional = models.CharField(max_length=50,
                                  help_text="Home functionality (assume typical unless deductions are warranted)")
    fireplaces = models.IntegerField(help_text="Number of fireplaces")
    fireplacequ = models.CharField(max_length=50, null=True, blank=True, help_text="Fireplace quality")
    garagetype = models.CharField(max_length=50, null=True, blank=True, help_text="Garage location")
    garageyrblt = models.IntegerField(null=True, blank=True, help_text="Year garage was built")
    garagefinish = models.CharField(max_length=50, null=True, blank=True, help_text="Interior finish of the garage")
    garagecars = models.IntegerField(null=True, blank=True, help_text="Size of garage in car capacity")
    garagesqft = models.IntegerField(null=True, blank=True, help_text="Size of garage in square feet")
    garagequal = models.CharField(max_length=50, null=True, blank=True, help_text="Garage quality")
    garagecond = models.CharField(max_length=50, null=True, blank=True, help_text="Garage condition")
    paveddrive = models.CharField(max_length=50, help_text="Paved driveway (Y/N)")
    wooddecksf = models.IntegerField(help_text="Wood deck area in square feet")
    openporchsf = models.IntegerField(help_text="Open porch area in square feet")
    enclosedporch = models.IntegerField(help_text="Enclosed porch area in square feet")
    threessnporch = models.IntegerField(help_text="Three season porch area in square feet")
    screenporch = models.IntegerField(help_text="Screen porch area in square feet")
    poolarea = models.IntegerField(help_text="Pool area in square feet")
    poolqc = models.CharField(max_length=50, null=True, blank=True, help_text="Pool quality")
    fence = models.CharField(max_length=50, null=True, blank=True, help_text="Fence quality")
    miscfeature = models.CharField(max_length=50, null=True, blank=True,
                                   help_text="Miscellaneous feature not covered in other categories")
    miscval = models.IntegerField(help_text="Value of miscellaneous feature")
    mosold = models.IntegerField(help_text="Month sold")
    yrsold = models.IntegerField(help_text="Year sold")
    saletype = models.CharField(max_length=50, help_text="Type of sale")
    salecondition = models.CharField(max_length=50, help_text="Condition of sale")
    saleprice = models.IntegerField(help_text="Sale price (in USD)")
    data_source = models.IntegerField(blank=False, null=False, default=1, help_text="Source of the data: 1 is Ames")

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return f"Property Pid{self.pid} - neighborhood: {self.neighborhood} - sale price: {self.saleprice}"