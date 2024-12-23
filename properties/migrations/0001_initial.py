# Generated by Django 5.1.4 on 2024-12-23 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pid', models.IntegerField(help_text='Parcel Identification Number')),
                ('mssubclass', models.IntegerField(help_text='The building class')),
                ('mszoning', models.CharField(help_text='General zoning classification', max_length=50)),
                ('lotfrontage', models.FloatField(blank=True, help_text='Linear feet of street connected to property', null=True)),
                ('lotarea', models.IntegerField(help_text='Lot size in square feet')),
                ('street', models.CharField(help_text='Type of road access', max_length=50)),
                ('alley', models.CharField(blank=True, help_text='Type of alley access', max_length=50, null=True)),
                ('lotshape', models.CharField(help_text='General shape of property', max_length=50)),
                ('landcontour', models.CharField(help_text='Flatness of the property', max_length=50)),
                ('utilities', models.CharField(help_text='Type of utilities available', max_length=50)),
                ('lotconfig', models.CharField(help_text='Lot configuration', max_length=50)),
                ('landslope', models.CharField(help_text='Slope of property', max_length=50)),
                ('neighborhood', models.CharField(help_text='Physical location within Ames', max_length=50)),
                ('condition1', models.CharField(help_text='Proximity to main road or railroad', max_length=50)),
                ('condition2', models.CharField(help_text='Proximity to main road or railroad (if a second exists)', max_length=50)),
                ('bldgtype', models.CharField(help_text='Type of dwelling', max_length=50)),
                ('housestyle', models.CharField(help_text='Style of dwelling', max_length=50)),
                ('overallqual', models.IntegerField(help_text='Overall material and finish quality')),
                ('overallcond', models.IntegerField(help_text='Overall condition rating')),
                ('yearbuilt', models.IntegerField(help_text='Original construction date')),
                ('yearremodadd', models.IntegerField(help_text='Remodel date (if applicable)')),
                ('roofstyle', models.CharField(help_text='Type of roof', max_length=50)),
                ('roofmatl', models.CharField(help_text='Roof material', max_length=50)),
                ('exterior1st', models.CharField(help_text='Exterior covering on house', max_length=50)),
                ('exterior2nd', models.CharField(help_text='Exterior covering on house (if more than one)', max_length=50)),
                ('masvnrtype', models.CharField(blank=True, help_text='Masonry veneer type', max_length=50, null=True)),
                ('masvnrarea', models.FloatField(blank=True, help_text='Masonry veneer area in square feet', null=True)),
                ('exterqual', models.CharField(help_text='Quality of exterior material', max_length=50)),
                ('extercond', models.CharField(help_text='Condition of exterior material', max_length=50)),
                ('foundation', models.CharField(help_text='Type of foundation', max_length=50)),
                ('bsmtqual', models.CharField(blank=True, help_text='Height of the basement', max_length=50, null=True)),
                ('bsmtcond', models.CharField(blank=True, help_text='General condition of the basement', max_length=50, null=True)),
                ('bsmtexposure', models.CharField(blank=True, help_text='Walkout or garden level basement walls exposure', max_length=50, null=True)),
                ('bsmtfintype1', models.CharField(blank=True, help_text='Finished basement area type 1', max_length=50, null=True)),
                ('bsmtfinsf1', models.IntegerField(blank=True, help_text='Type 1 finished square feet', null=True)),
                ('bsmtfintype2', models.CharField(blank=True, help_text='Finished basement area type 2', max_length=50, null=True)),
                ('bsmtfinsf2', models.IntegerField(blank=True, help_text='Type 2 finished square feet', null=True)),
                ('bsmtunfsf', models.IntegerField(blank=True, help_text='Unfinished square feet of basement area', null=True)),
                ('totalbsmtsf', models.IntegerField(blank=True, help_text='Total square feet of basement area', null=True)),
                ('heating', models.CharField(help_text='Type of heating', max_length=50)),
                ('heatingqc', models.CharField(help_text='Heating quality and condition', max_length=50)),
                ('centralair', models.CharField(help_text='Central air conditioning (Y/N)', max_length=1)),
                ('electrical', models.CharField(blank=True, help_text='Electrical system', max_length=50, null=True)),
                ('firstflrsf', models.IntegerField(help_text='First floor square feet')),
                ('secondflrsf', models.IntegerField(help_text='Second floor square feet')),
                ('lowqualfinsf', models.IntegerField(help_text='Low quality finished square feet (all floors)')),
                ('grlivarea', models.IntegerField(help_text='Above grade (ground) living area square feet')),
                ('bsmtfullbath', models.IntegerField(blank=True, help_text='Basement full bathrooms', null=True)),
                ('bsmthalfbath', models.IntegerField(blank=True, help_text='Basement half bathrooms', null=True)),
                ('fullbath', models.IntegerField(help_text='Full bathrooms above grade')),
                ('halfbath', models.IntegerField(help_text='Half baths above grade')),
                ('bedroomabvgr', models.IntegerField(help_text='Number of bedrooms above basement level')),
                ('kitchenabvgr', models.IntegerField(help_text='Number of kitchens')),
                ('kitchenqual', models.CharField(help_text='Kitchen quality', max_length=50)),
                ('totrmsabvgrd', models.IntegerField(help_text='Total rooms above grade (excluding bathrooms)')),
                ('functional', models.CharField(help_text='Home functionality (assume typical unless deductions are warranted)', max_length=50)),
                ('fireplaces', models.IntegerField(help_text='Number of fireplaces')),
                ('fireplacequ', models.CharField(blank=True, help_text='Fireplace quality', max_length=50, null=True)),
                ('garagetype', models.CharField(blank=True, help_text='Garage location', max_length=50, null=True)),
                ('garageyrblt', models.IntegerField(blank=True, help_text='Year garage was built', null=True)),
                ('garagefinish', models.CharField(blank=True, help_text='Interior finish of the garage', max_length=50, null=True)),
                ('garagecars', models.IntegerField(blank=True, help_text='Size of garage in car capacity', null=True)),
                ('garagesqft', models.IntegerField(blank=True, help_text='Size of garage in square feet', null=True)),
                ('garagequal', models.CharField(blank=True, help_text='Garage quality', max_length=50, null=True)),
                ('garagecond', models.CharField(blank=True, help_text='Garage condition', max_length=50, null=True)),
                ('paveddrive', models.CharField(help_text='Paved driveway (Y/N)', max_length=50)),
                ('wooddecksf', models.IntegerField(help_text='Wood deck area in square feet')),
                ('openporchsf', models.IntegerField(help_text='Open porch area in square feet')),
                ('enclosedporch', models.IntegerField(help_text='Enclosed porch area in square feet')),
                ('threessnporch', models.IntegerField(help_text='Three season porch area in square feet')),
                ('screenporch', models.IntegerField(help_text='Screen porch area in square feet')),
                ('poolarea', models.IntegerField(help_text='Pool area in square feet')),
                ('poolqc', models.CharField(blank=True, help_text='Pool quality', max_length=50, null=True)),
                ('fence', models.CharField(blank=True, help_text='Fence quality', max_length=50, null=True)),
                ('miscfeature', models.CharField(blank=True, help_text='Miscellaneous feature not covered in other categories', max_length=50, null=True)),
                ('miscval', models.IntegerField(help_text='Value of miscellaneous feature')),
                ('mosold', models.IntegerField(help_text='Month sold')),
                ('yrsold', models.IntegerField(help_text='Year sold')),
                ('saletype', models.CharField(help_text='Type of sale', max_length=50)),
                ('salecondition', models.CharField(help_text='Condition of sale', max_length=50)),
                ('saleprice', models.IntegerField(help_text='Sale price (in USD)')),
            ],
        ),
    ]
