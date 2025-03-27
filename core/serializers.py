from rest_framework import serializers
from .models import Plante, User, UserPlante

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'firstname', 'lastname', 'username', 'email', 'password']  # `user_id` ma primarykey
        extra_kwargs = {
            'user_id': {'read_only': True}, 
            'password': {'write_only': True},  
        }


class PlanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plante
        fields = ['plante_id', 'name', 'moisture_max', 'moisture_min']  

class UserPlanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlante
        fields = ['users_plantes_id', 'user', 'plante']