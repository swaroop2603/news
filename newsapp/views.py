from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from .models import User,News_paper,Comments
from .Serializers import userserializers,news_serializers,comment_serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from datetime import datetime
from dateutil import parser as date_parser
from rest_framework import serializers
from .pagination import CustomPagination

class login(GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                serializer = userserializers(user)
                payload={
                    'id':serializer.data.get('user_id'),
                    'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=15),
                    'iat':datetime.datetime.utcnow()
                }
                token=jwt.encode(payload,'secret',algorithm='HS256')
                response=Response()
                response.set_cookie(key='jwt',value=token,httponly=True)
                response.data={
                    'jwt':token
                }
                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            raise AuthenticationFailed('User not found')

class logout(GenericAPIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unautheticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = User.objects.get(user_id=payload['id'])
        serializer = userserializers(user)
        username=serializer.data.get('username')
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':f'{username} logged out successfully'
        }
        return response

class Signup(GenericAPIView):
    def post(self, request):
        serilizer = userserializers(data=request.data)
        if serilizer.is_valid():
            email = request.data.get("email")
            password = request.data.get("password")
            username = request.data.get('username')
            hash_password = make_password(password)
            try:
                user = User.objects.create(email=email, password=hash_password, username=username)
            except IntegrityError:

                return Response({"error": "User with this email already exists."},status=status.HTTP_400_BAD_REQUEST)

            serializer= userserializers(user)

            return Response({"message":"sigin successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

class news_details(GenericAPIView):
    pagination_class = CustomPagination
    def post(self,request):
        serializer = news_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        categary=request.query_params.get('categary')
        source=request.query_params.get('source')
        location=request.query_params.get('location')
        date=request.query_params.get('date')
        queryset=News_paper.objects.all()
        if categary:
            queryset = queryset.filter(categary=categary)

        if source:
            queryset = queryset.filter(source=source)
        if location:
            queryset = queryset.filter(location=location)
        if date:
            queryset = queryset.filter(date=date)
        page = self.paginate_queryset(queryset)
        serializer = news_serializers(page, many=True)
        offer_details_list = serializer.data
        return Response(offer_details_list)
    def put(self,request):
        paper_id=request.data.get('paper_id')


        try:
            target = News_paper.objects.get(paper_id=paper_id)
        except News_paper.DoesNotExist:
            return Response({"detail": " not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = news_serializers(target, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        paper_id=request.data.get('paper_id')
        try:
            target = News_paper.objects.get(paper_id=paper_id)
            target.delete()

            return Response({'message': 'news deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except News_paper.DoesNotExist:
            return Response({"detail": " not found."}, status=status.HTTP_404_NOT_FOUND)

class comments(GenericAPIView):
    def post(self,request):
        serializer = comment_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        paper_id=request.query_params.get('paper_id')
        target=Comments.objects.filter(paper_id=paper_id)
        return Response(target)