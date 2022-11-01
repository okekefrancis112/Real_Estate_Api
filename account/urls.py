from django.urls import path
from django.contrib.auth import views as auth_views



from .views import \
(
RegistrationAPIView,
UserRetrieveUpdateDeleteAPIView,
LoginAPIView
)
app_name='account'

urlpatterns = [

    path('create_realtor', RegistrationAPIView.as_view(), name='create_realtor'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('get_realtor', UserRetrieveUpdateDeleteAPIView.as_view(),name='get_realtor'),
    path('update_realtor', UserRetrieveUpdateDeleteAPIView.as_view(),name='update_realtor'),
    path('delete_realtor/<int:pk>', UserRetrieveUpdateDeleteAPIView.as_view(),name='delete_realtor')
]
 