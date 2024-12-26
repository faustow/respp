from rest_framework import serializers


class PredictPriceSerializer(serializers.Serializer):
    lotarea = serializers.FloatField()
    overallqual = serializers.IntegerField()
    overallcond = serializers.IntegerField()
    centralair = serializers.BooleanField()
    fullbath = serializers.IntegerField()
    bedroomabvgr = serializers.IntegerField()
    garagecars = serializers.IntegerField()
