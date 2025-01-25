from django.shortcuts import render
# from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view 
from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
from .models import Count_user, User_profil, User_plants
# from .supabase_utils import fetch_from_supabase, insert_to_supabase, new_insert_to_supabase, delete_from_supabase, getuserby_Id_from_supabase,getuserPost_by_Id_from_supabase,updateuser_profil_by_Id_from_supabase
from django.utils import timezone
from datetime import datetime

@api_view(['POST'])
def create_user(request):
    data = request.data



