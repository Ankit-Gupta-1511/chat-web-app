
from rest_framework import serializers
from .models import Input, User, Response, Query

class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the USer instance into JSON format."""
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = ('id', 'username', 'date_of_creation')
        read_only_fields = ('date_of_creation')

class InputSerializer(serializers.ModelSerializer):
    """Serializer to map the Input instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Input
        fields = ('id', 'msg', 'pub_date')
        read_only_fields = ('pub_date')

class ResponseSerializer(serializers.ModelSerializer):
    """Serializer to map the Response instance into JSON format."""
    input_msg = serializers.ReadOnlyField(source='input_msg.id')
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Response
        fields = ('id', 'response', 'input_msg')

class QuerySerializer(serializers.ModelSerializer):
    """Serializer to map the Response instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Query
        fields = ('id', 'email', 'query')        

