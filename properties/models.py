import uuid

from django.db import models


class Property(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the property"
    )
    pid = models.IntegerField(help_text="Parcel Identification Number", null=True, blank=True)
    mssubclass = models.IntegerField(help_text="The building class", null=True, blank=True)
    mszoning = models.CharField(max_length=50, help_text="General zoning classification", null=True, blank=True)
    lotfrontage = models.FloatField(null=True, blank=True, help_text="Linear feet of street connected to property")
    lotarea = models.IntegerField(help_text="Lot size in square feet")
    street = models.CharField(max_length=50, help_text="Type of road access", null=True, blank=True)
    alley = models.CharField(max_length=50, null=True, blank=True, help_text="Type of alley access")
    lotshape = models.CharField(max_length=50, help_text="General shape of property", null=True, blank=True)
    landcontour = models.CharField(max_length=50, help_text="Flatness of the property", null=True, blank=True)
    utilities = models.CharField(max_length=50, help_text="Type of utilities available", null=True, blank=True)
    lotconfig = models.CharField(max_length=50, help_text="Lot configuration", null=True, blank=True)
    landslope = models.CharField(max_length=50, help_text="Slope of property", null=True, blank=True)
    neighborhood = models.CharField(max_length=50, help_text="Physical location within Ames", null=True, blank=True)
    condition1 = models.CharField(max_length=50, help_text="Proximity to main road or railroad", null=True, blank=True)
    condition2 = models.CharField(max_length=50, help_text="Proximity to main road or railroad (if a second exists)",
                                  null=True, blank=True)
    bldgtype = models.CharField(max_length=50, help_text="Type of dwelling", null=True, blank=True)
    housestyle = models.CharField(max_length=50, help_text="Style of dwelling", null=True, blank=True)
    overallqual = models.IntegerField(help_text="Overall material and finish quality")
    overallcond = models.IntegerField(help_text="Overall condition rating")
    yearbuilt = models.IntegerField(help_text="Original construction date", null=True, blank=True)
    yearremodadd = models.IntegerField(help_text="Remodel date (if applicable)", null=True, blank=True)
    roofstyle = models.CharField(max_length=50, help_text="Type of roof", null=True, blank=True)
    roofmatl = models.CharField(max_length=50, help_text="Roof material", null=True, blank=True)
    exterior1st = models.CharField(max_length=50, help_text="Exterior covering on house", null=True, blank=True)
    exterior2nd = models.CharField(max_length=50, help_text="Exterior covering on house (if more than one)", null=True,
                                   blank=True)
    masvnrtype = models.CharField(max_length=50, null=True, blank=True, help_text="Masonry veneer type")
    masvnrarea = models.FloatField(null=True, blank=True, help_text="Masonry veneer area in square feet")
    exterqual = models.CharField(max_length=50, help_text="Quality of exterior material", null=True, blank=True)
    extercond = models.CharField(max_length=50, help_text="Condition of exterior material", null=True, blank=True)
    foundation = models.CharField(max_length=50, help_text="Type of foundation", null=True, blank=True)
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
    heating = models.CharField(max_length=50, help_text="Type of heating", null=True, blank=True)
    heatingqc = models.CharField(max_length=50, help_text="Heating quality and condition", null=True, blank=True)
    centralair = models.IntegerField(help_text="Central air conditioning (1/0)")
    electrical = models.CharField(max_length=50, null=True, blank=True, help_text="Electrical system")
    firstflrsf = models.IntegerField(help_text="First floor square feet", null=True, blank=True)
    secondflrsf = models.IntegerField(help_text="Second floor square feet", null=True, blank=True)
    lowqualfinsf = models.IntegerField(help_text="Low quality finished square feet (all floors)", null=True, blank=True)
    grlivarea = models.IntegerField(help_text="Above grade (ground) living area square feet", null=True, blank=True)
    bsmtfullbath = models.IntegerField(null=True, blank=True, help_text="Basement full bathrooms")
    bsmthalfbath = models.IntegerField(null=True, blank=True, help_text="Basement half bathrooms")
    fullbath = models.IntegerField(help_text="Full bathrooms above grade")
    halfbath = models.IntegerField(help_text="Half baths above grade", null=True, blank=True)
    bedroomabvgr = models.IntegerField(help_text="Number of bedrooms above basement level")
    kitchenabvgr = models.IntegerField(help_text="Number of kitchens", null=True, blank=True)
    kitchenqual = models.CharField(max_length=50, help_text="Kitchen quality", null=True, blank=True)
    totrmsabvgrd = models.IntegerField(help_text="Total rooms above grade (excluding bathrooms)", null=True, blank=True)
    functional = models.CharField(max_length=50, null=True, blank=True,
                                  help_text="Home functionality (assume typical unless deductions are warranted)")
    fireplaces = models.IntegerField(help_text="Number of fireplaces", null=True, blank=True)
    fireplacequ = models.CharField(max_length=50, null=True, blank=True, help_text="Fireplace quality")
    garagetype = models.CharField(max_length=50, null=True, blank=True, help_text="Garage location")
    garageyrblt = models.IntegerField(null=True, blank=True, help_text="Year garage was built")
    garagefinish = models.CharField(max_length=50, null=True, blank=True, help_text="Interior finish of the garage")
    garagecars = models.IntegerField(help_text="Size of garage in car capacity", default=0)
    garagesqft = models.IntegerField(null=True, blank=True, help_text="Size of garage in square feet")
    garagequal = models.CharField(max_length=50, null=True, blank=True, help_text="Garage quality")
    garagecond = models.CharField(max_length=50, null=True, blank=True, help_text="Garage condition")
    paveddrive = models.CharField(max_length=50, null=True, blank=True, help_text="Paved driveway (Y/N)")
    wooddecksf = models.IntegerField(help_text="Wood deck area in square feet", null=True, blank=True)
    openporchsf = models.IntegerField(help_text="Open porch area in square feet", null=True, blank=True)
    enclosedporch = models.IntegerField(help_text="Enclosed porch area in square feet", null=True, blank=True)
    threessnporch = models.IntegerField(help_text="Three season porch area in square feet", null=True, blank=True)
    screenporch = models.IntegerField(help_text="Screen porch area in square feet", null=True, blank=True)
    poolarea = models.IntegerField(help_text="Pool area in square feet", null=True, blank=True)
    poolqc = models.CharField(max_length=50, null=True, blank=True, help_text="Pool quality")
    fence = models.CharField(max_length=50, null=True, blank=True, help_text="Fence quality")
    miscfeature = models.CharField(max_length=50, null=True, blank=True,
                                   help_text="Miscellaneous feature not covered in other categories")
    miscval = models.IntegerField(help_text="Value of miscellaneous feature", null=True, blank=True)
    mosold = models.IntegerField(help_text="Month sold", null=True, blank=True)
    yrsold = models.IntegerField(help_text="Year sold", null=True, blank=True)
    saletype = models.CharField(max_length=50, help_text="Type of sale", null=True, blank=True)
    salecondition = models.CharField(max_length=50, help_text="Condition of sale", null=True, blank=True)
    saleprice = models.IntegerField(help_text="Sale price (in USD)")
    data_source = models.IntegerField(blank=False, null=False, default=1, help_text="1=Ames, 2=Verified Sale")
    dataset = models.CharField(
        max_length=10,
        choices=[("training", "Training"), ("validation", "Validation"), ("test", "Test")],
        default="training",
    )

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return f"Property Pid{self.pid} - Price: {self.saleprice} (source={self.data_source},dataset={self.dataset})"


class Listing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="listings")
    description = models.TextField(help_text="User-provided basic description of the best features of the property")
    generated_text = models.TextField(help_text="LLM-generated salesy listing for the property")
    feedback_score = models.FloatField(
        null=True, blank=True,
        help_text="Score for RLHF (e.g., 1 for thumbs up, -1 for thumbs down)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing for Property {self.property.id} created on {self.created_at}"
