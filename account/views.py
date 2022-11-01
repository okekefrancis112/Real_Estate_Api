from sqlite3 import IntegrityError
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.core.cache import cache
# from django.core import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import User
from goldapi.utils import get_ip,generate_referral_code
from goldapi.models import Realtor
from django.utils.decorators import method_decorator
from django.db.transaction import atomic


from .serializers import (RegistrationSerializer,LoginSerializer,UserSerializer)
from goldapi.serializers import RealtorSerializer


@method_decorator(atomic, name='dispatch')
class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    realtor_class = RealtorSerializer
    def post(self, request):
        password = request.data.get('password', {})
        # email = request.data.get('email', {})
        confirm_password=request.data.get('confirm_password',{})
        if password == confirm_password:
            try:
                serializer = self.serializer_class(data=request.data['user'])
                serializer.is_valid(raise_exception=True)
                realtor_serializer = self.realtor_class(data=request.data['realtor'])
                request.data['realtor'].update({"realtor":request.data['user'],"referral_code":request.data['user']['username'] + "_" + generate_referral_code()})
                if realtor_serializer.is_valid():
                    print("Realtor true",realtor_serializer.is_valid())
                    serializer.save(ip_address=get_ip(request))
                    realtor_serializer.save(realtor=User.objects.get(username=serializer.data['username']))
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(realtor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except IntegrityError as e:
                print("There is error somewhere",e.message)
                return Response(realtor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return  Response('Passwords must match')


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print("Data request",request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    # def get_queryset(self):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        
        # if(request.user.is_superuser):
        #     if 'provider' in cache:
        #         # get results from cache
        #         providers = cache.get('provider')
        #         return Response(providers, status=status.HTTP_201_CREATED)

                # pk = self.kwargs["pk"]
                # return get_object_or_404(User, pk=pk)
                # serialized_provider = serialized_obj = serializers.serialize('python',realtor)
                # results = [provider for provider in serialized_provider]
                # store data in cache
                # cache.set("provider",results, timeout=CACHE_TTL)
   

    def update(self, request, *args, **kwargs):
        serializer_data = {
            'username': request.data.get('username', request.user.username),
            'email': request.data.get('email', request.user.email),
        }
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete_user = get_object_or_404(User, pk=pk)
        delete_user.delete()
        return Response({"message": "Your account has been deleted.".format(pk)},status=204)