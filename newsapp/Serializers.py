from rest_framework import serializers
from .models import User,News_paper,Comments
class userserializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['user_id','username','email']



class news_serializers(serializers.ModelSerializer):
    class Meta:
        model=News_paper
        fields='__all__'

class comment_serializers(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields='__all__'