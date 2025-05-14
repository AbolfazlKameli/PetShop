from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from petshop.utils.doc_serializers import ResponseSerializer
from petshop.utils.exceptions import CustomBadRequest
from petshop.utils.permissions import IsOwnerUser
from ..models import Address
from ..selectors import get_all_addresses, get_user_addresses
from ..serializers import AddressSerializer


@extend_schema(tags=['Addresses'])
class UserAddressesListAPI(ListAPIView):
    """
    API for listing authenticated users addresses. Accessible only to the uesr themselves.
    """
    serializer_class = AddressSerializer
    permission_classes = (IsOwnerUser,)
    search_fields = ('address', 'postal_code')

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Address.objects.none()
        return get_user_addresses(owner=self.request.user)


@extend_schema(tags=['Addresses'])
class AddressCreateAPI(GenericAPIView):
    """
    API for creating addresses for the authenticated user. Accessible only to the user themselves.
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={201: ResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                data={'data': {'message': 'address created successfully.'}},
                status=status.HTTP_201_CREATED
            )
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Addresses'])
class AddressUpdateAPI(GenericAPIView):
    """
    API for updating addresses for the authenticated user. Accessible only to the user themselves.
    """
    serializer_class = AddressSerializer
    permission_classes = (IsOwnerUser,)
    lookup_url_kwarg = 'address_id'
    queryset = get_all_addresses()

    @extend_schema(responses={200: ResponseSerializer})
    def put(self, request, *args, **kwargs):
        address = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=address)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'data': {'message': 'address updated successfully.'}},
                status=status.HTTP_200_OK
            )
        raise CustomBadRequest(serializer.errors)


@extend_schema(tags=['Addresses'])
class AddressDeleteAPI(GenericAPIView):
    """
    API for deleting addresses for the authenticated user. Accessible only to the user themselves.
    """
    serializer_class = AddressSerializer
    permission_classes = (IsOwnerUser,)
    lookup_url_kwarg = 'address_id'
    queryset = get_all_addresses()

    def delete(self, request, *args, **kwargs):
        address = self.get_object()
        address.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
