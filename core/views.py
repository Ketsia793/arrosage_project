from rest_framework import viewsets
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Plante, UserPlante
from .serializers import UserSerializer, PlanteSerializer, UserPlanteSerializer

# Vue pour la création d'un utilisateur 
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue pour les utilisateurs (avec ModelViewSet, qui gère CRUD)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Vue pour les plantes
class PlanteViewSet(viewsets.ModelViewSet):
    queryset = Plante.objects.all()
    serializer_class = PlanteSerializer


# Sérialiseur pour associer un User et une Plante
class UserPlanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlante
        fields = ['users_plantes_id', 'user', 'plante']


# Vue pour la relation entre un user et sa plante
class LinkUserToPlanteAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Récupérer les IDs des données envoyées
        user_id = request.data.get('user_id')
        plante_id = request.data.get('plante_id')

        # Vérification si les ID sont valides (entiers)
        if not isinstance(user_id, int) or not isinstance(plante_id, int):
            return Response({"error": "user_id and plante_id must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'utilisateur et la plante existent
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            plante = Plante.objects.get(plante_id=plante_id)
        except Plante.DoesNotExist:
            return Response({"error": "Plante not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si la relation existe déjà
        if UserPlante.objects.filter(user=user, plante=plante).exists():
            return Response({"error": "This user is already linked to this plant."}, status=status.HTTP_400_BAD_REQUEST)

        # Créer une relation entre l'utilisateur et la plante
        user_plante = UserPlante.objects.create(user=user, plante=plante)

        # Sérialiser la relation et retourner la réponse
        serializer = UserPlanteSerializer(user_plante)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UpdatePlanteDataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Récupérer les IDs des données envoyées
        plante_id = request.data.get('plante_id')
        temperature = request.data.get('temperature')
        humidity = request.data.get('humidity')

        # Vérification que les données sont présentes et valides
        if not isinstance(plante_id, int):
            return Response({"error": "plante_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(temperature, (int, float)) or not isinstance(humidity, (int, float)):
            return Response({"error": "Temperature and humidity must be valid numbers."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plante = Plante.objects.get(plante_id=plante_id)
        except Plante.DoesNotExist:
            return Response({"error": "Plante not found"}, status=status.HTTP_404_NOT_FOUND)

        # Màj des données de temp et d'humidité dans la plante
        plante.moisture_max = humidity  
        plante.moisture_min = temperature 
        plante.save()  

        # Retourner une réponse de succès
        return Response({"success": "Plante data updated successfully"}, status=status.HTTP_200_OK)