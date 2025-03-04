from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime
from .models import CountUser, UserPlant  
from .supabaseUtils import (
    fetch_from_supabase,
    insert_to_supabase,
    new_insert_to_supabase,
    delete_from_supabase,
    getuserby_Id_from_supabase,
    getuserPost_by_Id_from_supabase,
    updateuser_profil_by_Id_from_supabase,
)

@api_view(['POST'])
def create_user(request):
    data = request.data

    # Récupérer et nettoyer les données
    last_name = data.get('last_name', '').strip()
    first_name = data.get('first_name', '').strip()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Vérification des champs requis
    if not email or not password:
        return Response({"error": "Email et mot de passe sont obligatoires"}, status=status.HTTP_400_BAD_REQUEST)

    # Vérification de l'unicité de l'email et du nom d'utilisateur
    if CountUser.objects.filter(username=username).exists():
        return Response({"error": "Ce nom d'utilisateur est déjà pris."}, status=status.HTTP_400_BAD_REQUEST)

    if CountUser.objects.filter(email=email).exists():
        return Response({"error": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

    # Hash du mot de passe
    hashed_password = make_password(password)

    # Création de l'utilisateur
    try:
        user = CountUser.objects.create(
            username=username,
            last_name=last_name,
            first_name=first_name,
            email=email,
            password=hashed_password,
            is_staff=False,
            is_active=True,  # L'utilisateur peut être actif dès la création
            is_superuser=False,
            date_joined=timezone.now()
        )
    except IntegrityError as e:
        return Response({"error": "Erreur de contrainte d'intégrité lors de la création de l'utilisateur", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "Erreur lors de la création de l'utilisateur", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        user_plant = UserPlant.objects.create(
            user=user,
            name="Plante par défaut",
            image='default.jpg',
            created_at=timezone.now()
        )
    except Exception as e:
        return Response({"error": "Erreur lors de la création de la plante par défaut", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Retourner la réponse de succès
    return Response({'user': user.id, 'user_plant': user_plant.id}, status=status.HTTP_201_CREATED)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_plant(request):
    user = request.user  # L'utilisateur actuel à partir du token JWT
    data = request.data
    
    # Assurez-vous que les données essentielles sont présentes
    name = data.get('name')
    image = data.get('image')

    if not name:
        return Response({"detail": "Le nom de la plante est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Créer une nouvelle instance de UserPlant
    plant = UserPlant.objects.create(
        user=user,  # Lier la plante à l'utilisateur actuel
        name=name,
        image=image or 'default.jpg',  # Fournir une image par défaut si aucune image n'est donnée
    )
    
    # Retourner la réponse avec les données de la nouvelle plante
    return Response({
        "plant_id": plant.plant_id,
        "user_id": plant.user.id,
        "name": plant.name,
        "image": plant.image.url,
        "created_at": plant.created_at,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profil(request):
    request.data["user_id"] = request.user.id 
    data = request.data 
    profil = getuserPost_by_Id_from_supabase('auto_water_system_app_UserProfile', data)
    print(profil)
    return Response(profil)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def put_user_profil(request):
    request.data["user_id"] = request.user.id
    data = request.data 
    profil = getuserPost_by_Id_from_supabase('auto_water_system_app_UserProfile', data)
    request.data["profil_id"] = profil['details'][0]['profil_id']
    request.data["image"] = profil['details'][0]['image']
    request.data["created_at"] = profil['details'][0]['created_at']
    request.data["username"] = profil['details'][0]['username']
    data = request.data 
    profil = updateuser_profil_by_Id_from_supabase('auto_water_system_app_UserProfile', data)
    print(f"Ceci est le profil{profil}")
    return Response(profil)


@api_view(['POST'])
def delete_user(request):
    data = request.data
    user = delete_from_supabase('auto_water_system_app_CountUser', data)
    return Response(user)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_userId(request):
    print(f"voici l'id {request.user.id} ")
    # grâce à request.user.id = accès à l'id via le token 
    request.data["id"] = request.user.id 
    data = request.data 
    # pour afficher les infos de l'utilisateur, son id est nécessaire 
    # que l'on obtient grâce à request.user.id qui est contenu dans le token 
    newPlantInfo = getuserby_Id_from_supabase('auto_water_system_app_CountUser', data)
    return Response(newPlantInfo)

@api_view(['GET'])
def get_user(request):
    users = fetch_from_supabase('auto_water_system_app_CountUser')
    return Response(users)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_profile(request):
    request.data["user_id"] = request.user.id
    request.data["created_at"] = datetime.now().date().isoformat()
    data = request.data
    profil = getuserPost_by_Id_from_supabase('auto_water_system_app_UserProfile', data)
    print(f"profile = {profil}")
    data['username'] = profil['details'][0]['username']
    newPlantInfo = insert_to_supabase('auto_water_system_app_UserPlant', data)
    return Response(newPlantInfo)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_plants(request):
    PlantsInfos = fetch_from_supabase('auto_water_system_app_UserPlant')
    return Response(PlantsInfos)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_plant(request):
    request.data["user_id"] = request.user.id 
    data = request.data 
    PlantsInfos = getuserPost_by_Id_from_supabase('auto_water_system_app_UserPlant', data)
    print(PlantsInfos)
    return Response(PlantsInfos)

