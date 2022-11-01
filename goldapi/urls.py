from django.urls import path
# from django.contrib.auth import views as auth_views



from .views import \
(
RealtorRetrieveUpdateDeleteAPIView,
PropertyAPIView,
PropertyRetrieveUpdateDeleteAPIView
)
app_name='goldapi'

urlpatterns = [

    # path('create_realtor', RegistrationAPIView.as_view(), name='create_realtor'),
    path('properties', PropertyRetrieveUpdateDeleteAPIView.as_view(), name='properties'),
    path('create_properties', PropertyAPIView.as_view(), name='properties'),
    path('details', RealtorRetrieveUpdateDeleteAPIView.as_view(),name='realtor_details'),
    # path('update_realtor', UserRetrieveUpdateDeleteAPIView.as_view(),name='update_realtor'),
    # path('delete_realtor/<int:pk>', UserRetrieveUpdateDeleteAPIView.as_view(),name='delete_realtor')
]
 