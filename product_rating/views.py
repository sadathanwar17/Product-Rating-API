from rest_framework import generics
from .serializers import ProductSerializer, UserSerializer, UserProductSerializer
from .models import Product_Table, Product_User_Table
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class CreateView(generics.ListCreateAPIView):
    queryset = Product_Table.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response("Unauthorised to perform this action",status=HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"list": serializer.data, "username":request.user.username, "is_admin": request.user.is_staff}, status=HTTP_200_OK)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product_Table.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser, )

    def destroy(self, request, *args, **kwargs):
        prod_id = kwargs.get('pk')
        if Product_User_Table.objects.all().filter(product_id=prod_id).exists():
            prod = Product_User_Table.objects.all().filter(product_id=prod_id)
            for p in prod:
                p.user.remove(request.user)
                p.delete()
        if Product_Table.objects.all().filter(id=prod_id).exists():
            Product_Table.objects.all().get(id=prod_id).delete()
            return Response({"Successfully Deleted"}, status=HTTP_204_NO_CONTENT)
        return Response({"Object Not Found"}, status=HTTP_400_BAD_REQUEST)

class UserView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer

class BuyView(generics.ListCreateAPIView):
    serializer_class = UserProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        q = []
        if Product_User_Table.objects.filter(product_id=kwargs.get('pk'),user=request.user).exists():
            q = Product_User_Table.objects.get(product_id=kwargs.get('pk'), user=request.user)
        query = Product_Table.objects.get(id=request.data.get('product_id'))
        if (query.product_quantity == 0):
            return Response({"Bad Request"}, status=HTTP_400_BAD_REQUEST)
        query.product_quantity = query.product_quantity - 1
        query.save()
        if q:
            q.product_quantity = q.product_quantity + 1
            q.save()
            return Response({"Created"}, status=HTTP_201_CREATED)
        else:
            serializer = UserProductSerializer(data=request.data)
            if serializer.is_valid():
                prop = serializer.save()
                prop.user.add(request.user)
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        return Product_User_Table.objects.filter(user=user)

@api_view(["POST"])
def LoginView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"Error: Login Failed"}, status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "admin": user.is_staff}, status=HTTP_200_OK)

class RateProduct(generics.UpdateAPIView):
    serializer_class = UserProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        if Product_User_Table.objects.filter(product_id=kwargs.get('pk'),user=self.request.user).exists():
            query = Product_User_Table.objects.get(product_id=kwargs.get('pk'),user=self.request.user)
            if request.data.get('product_ratings') < 0 or request.data.get('product_ratings') > 5:
                return Response({"Bad Request"}, status=HTTP_400_BAD_REQUEST)
            query.product_ratings = request.data.get('product_ratings')
            query.save()
            q = Product_Table.objects.get(id=kwargs.get('pk'))
            q.ratings_count = q.ratings_count + 1
            q.ratings_sum = q.ratings_sum + request.data.get('product_ratings')
            q.ratings_average = round(q.ratings_sum / q.ratings_count,2)
            q.save()
            return Response({"product_id":int(kwargs.get('pk')), "product_ratings": request.data.get('product_ratings')}, status=HTTP_202_ACCEPTED)
        return Response("Unauthorised to perform this action", status=HTTP_401_UNAUTHORIZED)

class VerifyAdmin(APIView):
    def get(self, request, *args, **kwargs):
        token = kwargs.pop('token')
        user = Token.objects.get(key=token).user
        return Response({"is_admin":user.is_staff}, status=HTTP_200_OK);





