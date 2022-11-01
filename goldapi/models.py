from django.db import models
from django.conf import settings
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video

from account.models import User,TimestampedModel



GENDER = (
        ('None','None'),
        ('Male','Male'),
        ('Female', 'Female'),
    )


PROPERTY_TYPE= (
        ('None','None'),
        ('Land','Land'),
        ('Buildings', 'Buildings'),
    )


class Realtor(TimestampedModel):
    realtor = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank = True,related_name='realtor')
    first_name = models.CharField(max_length=150,default='')
    last_name = models.CharField(max_length=150,default='')
    address = models.CharField(max_length=500,default='')
    state_of_origin = models.CharField(max_length=500,default='')
    account_merchant = models.CharField(max_length=500,default='')
    account_number = models.CharField(max_length=500,default='',unique=True)
    date_of_birth = models.DateField()
    mobile= models.CharField(max_length=13,unique=True)
    gender= models.CharField(max_length=15, choices=GENDER,default='None')
    referral_code = models.CharField(max_length=40,default='',unique=True)
    referral = models.CharField(max_length=50,default='',blank=True,null=True)



    def __str__(self):
        return self.first_name + self.last_name


class RealtorClient(TimestampedModel):
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, null=True, blank = True)
    # property = models.ForeignKey(, on_delete=models.CASCADE, null=True, blank = True)
    full_name = models.CharField(max_length=150,default='')
    email = models.CharField(max_length=150,default='',unique=True)
    mobile = models.CharField(max_length=13,default='',unique=True)
    referral_code = models.CharField(max_length=40,default='')

    def __str__(self):
        return "Client name is " + self.full_name 


class Reward(TimestampedModel):
    FIFTEEN = 1
    THREE = 2
        
    REWARD_PERCENTAGE_CHOICES = (
        (FIFTEEN, '15'),
        (THREE, '3'),
    )
    realtor = models.OneToOneField(Realtor, on_delete=models.CASCADE, null=True, blank = True)
    current_reward_percentage = models.PositiveSmallIntegerField(choices=REWARD_PERCENTAGE_CHOICES, blank=True, null=True)
    fifteen_percent_unit = models.PositiveSmallIntegerField(default=0)
    three_percent_unit = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{} currently on {} percentage reward".format(self.realtor.first_name,self.current_reward_percentage)


class Property(TimestampedModel):
    property_name = models.CharField(max_length=500,null=False)
    image = models.ImageField(upload_to='media/properties')
    video = models.FileField(upload_to='media/properties/videos',blank=True,storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])
    property_id = models.CharField(max_length=50, default='',null=True,blank=True)
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPE,default='None')
    location = models.CharField(max_length=500,default='',null=False)
    no_of_unit_or_plot = models.PositiveSmallIntegerField(default=0)
    price_per_unit_plot = models.CharField(max_length=15,default='')
    on_promo = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    promo_price_per_unit_or_plot = models.CharField(max_length=15,default='',blank=True,null=True)

    # def save(self, *args, **kwargs):
    #     if self.property_name is not None:
    #         self.property_id = "{}_{}".format(self.property_name.lower(), generate_referral_code())
    #     super(Property, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        print("Update sales",kwargs['no_of_unit_or_plot'])
        unit_status = kwargs['no_of_unit_or_plot'] < self.no_of_unit_or_plot
        if unit_status:
            self.no_of_unit_or_plot = self.no_of_unit_or_plot - kwargs['no_of_unit_or_plot']
        else:
            return "Cannot sell at the moment. Units left is lesser than what is to be sold"
        super(Property, self).update(*args, **kwargs)

    def __str__(self):
        if self.on_promo:
            return "Property {} on promo going for {}".format(self.property_name,self.promo_price_per_unit_or_plot)
        return "Property {} going for {}".format(self.property_name,self.price_per_unit_plot) 


class NowSelling(TimestampedModel):
    property_name = models.CharField(max_length=500,null=False)
    image = models.ImageField(upload_to='media/properties')
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPE,default='None')
    info = models.TextField(default="")
    title = models.CharField(max_length=80,default="",blank=True)
    location = models.CharField(max_length=500,default='',null=False)
    unit_of_plot = models.PositiveSmallIntegerField(default=0)
    price_per_unit_plot = models.CharField(max_length=15,default='')
    on_promo = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_sold_out =  models.BooleanField(default=False)
    promo_price_per_unit_or_plot = models.CharField(max_length=15,default='',blank=True,null=True)

    # def save(self, *args, **kwargs):
    #     if self.property_name is not None:
    #         print("Am here")
    #         self.property_id = "{}_{}".format(self.property_name.lower(), generate_referral_code())
    #     super(Property, self).save(*args, **kwargs)

    # def update(self, *args, **kwargs):
    #     print("Update sales",kwargs['no_of_unit_or_plot'])
    #     unit_status = kwargs['no_of_unit_or_plot'] < self.no_of_unit_or_plot
    #     if unit_status:
    #         self.no_of_unit_or_plot = self.no_of_unit_or_plot - kwargs['no_of_unit_or_plot']
    #     else:
    #         return "Cannot sell at the moment. Units left is lesser than what is to be sold"
    #     super(Property, self).update(*args, **kwargs)

    def __str__(self):
        if self.on_promo:
            return "Property {} on promo going for {}".format(self.property_name,self.promo_price_per_unit_or_plot)
        return "Property {} going for {}".format(self.property_name,self.price_per_unit_plot) 


class SoldProperty(TimestampedModel):
    property_name = models.CharField(max_length=500,null=False)
    # image = models.ImageField(upload_to='media/properties')
    property_id = models.CharField(max_length=50, default='')
    property_type = models.CharField(max_length=15, choices=GENDER,default='None')
    location = models.CharField(max_length=500,default='',null=False)
    no_of_unit_or_plot = models.PositiveSmallIntegerField(default=0)
    price_per_unit_plot = models.CharField(max_length=15,default='')
    on_promo = models.BooleanField(default=False)
    promo_price_per_unit_or_plot = models.CharField(max_length=15,default='',blank=True,null=True)


    def __str__(self):
            return "Property {} was sold on {}. {} units".format(self.property_name,self.no_of_unit_or_plot)




