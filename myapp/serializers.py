from rest_framework import serializers
from .models import Sloves

class SlovesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sloves
        fields = ['id', 'name', 'price', 'desc', 'image', 'birth']
