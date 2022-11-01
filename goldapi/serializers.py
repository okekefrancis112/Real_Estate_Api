from sqlite3 import IntegrityError
from rest_framework import serializers
from .models import Realtor,Property
from account.serializers import UserSerializer
from django.core.files.base import ContentFile
import base64
import uuid
from rest_framework.fields import Field
from rest_framework.exceptions import APIException
class Base64ContentField(Field):
    """
    For image, send base64 string as json
    """

    def to_internal_value(self, data):
        try:
            format, datastr = data.split(';base64,')
            ext = format.split('/')[-1]
            file = ContentFile(base64.b64decode(datastr), name=str(uuid.uuid4())+'.'+ext)
        except:
            raise serializers.ValidationError('Error in decoding base64 data')
        return file

    def to_representation(self, value):
        if not value:
            return None
        return value.url



class RealtorSerializer(serializers.ModelSerializer):
    realtor = UserSerializer()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    state_of_origin = serializers.CharField(max_length=255)
    account_merchant = serializers.CharField(max_length=255)
    account_number = serializers.CharField(max_length=255)
    date_of_birth = serializers.CharField(max_length=255)
    mobile = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    referral_code = serializers.CharField(max_length=255)
    referral = serializers.CharField(max_length=255,allow_blank=True)


    class Meta:
        model = Realtor
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['realtor','first_name', 'last_name','address','state_of_origin','account_merchant','account_number','date_of_birth','mobile','gender',"referral_code","referral"]

    def validate_mobile(self,data):
        try:
            Realtor.objects.get(mobile=data)
        except:
            return data
        else:
            raise serializers.ValidationError("mobile number already exists")


    def validate_account_number(self,data):
        try:
            Realtor.objects.get(account_number=data)
        except:
            return data
        else:
            raise serializers.ValidationError("account number already exists")
       

    def create(self, validated_data):
        return Realtor.objects.create(**validated_data)



    def update(self, instance, validated_data):
        """Performs an update on a Realtor."""

        realtor_user = validated_data.pop('realtor', {})
        filter_data = ['referral','referral_code']
        for data in filter_data:
            validated_data.pop(data, {})


        


        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `Realtor` instance one at a time.
            setattr(instance.realtor, key, value)

        instance.realtor.save()

        realtor_user.pop('username',{})
        for (key, value) in realtor_user.items():
        # We're doing the same thing as above, but this time we're making
        # changes to the Realtor model.
            setattr(instance, key, value)

            # Save the profile just like we saved the realtor.
            instance.save()

        return instance.realtor


class PropertySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    property_name = serializers.CharField(max_length=255)
    image = Base64ContentField(required=False)
    video = Base64ContentField(required=False)
    property_id= serializers.CharField(max_length=255)
    property_type = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    no_of_unit_or_plot = serializers.CharField(max_length=255)
    price_per_unit_plot = serializers.CharField(max_length=255)
    is_popular = serializers.CharField(max_length=255)
    promo_price_per_unit_or_plot = serializers.CharField(max_length=255,allow_blank=True)



    class Meta:
        model = Property
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id','property_name','image','video','property_id','property_type','location','no_of_unit_or_plot','price_per_unit_plot','is_popular','promo_price_per_unit_or_plot']


    def create(self, validated_data):

        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Performs an update on a Property."""

        validated_data.pop('property_id', {})

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `Property` instance one at a time.
            setattr(instance, key, value)

        instance.save()

        return instance
