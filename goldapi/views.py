from django.conf import settings
# from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from goldapi.utils import generate_referral_code
# from rest_framework.parsers import MultiPartParser, FormParser

from .models import Realtor,Property


from .serializers import (RealtorSerializer,PropertySerializer)

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class RealtorRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RealtorSerializer
    def retrieve(self, request, *args, **kwargs):
        qs = Realtor.objects.get(realtor=request.user)
        serializer = self.serializer_class(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Partial update of the data
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PropertyRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer
    def retrieve(self, request, *args, **kwargs):
        qs = Property.objects.all()
        serializer = self.serializer_class(qs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Partial update of the data
        if_video = request.data['video']
        if not if_video:
            request.data.pop('video')
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    # parser_classes = (MultiPartParser, FormParser)
    # permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer
    def post(self, request):
            if_video = request.data['video']
            if not if_video:
                request.data.pop('video')
            serializer = self.serializer_class(data=request.data)
            request.data.update({"property_id":"property_" +  generate_referral_code()})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
