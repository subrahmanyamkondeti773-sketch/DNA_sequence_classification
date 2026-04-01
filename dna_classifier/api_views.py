from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from rest_framework import status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .models import DNASequence
from .serializers import UserSerializer, DNASequenceSerializer
from .utils import clean_sequence, validate_sequence
from .predictor import get_predictor
from .ai_helper import get_ai_explanation, get_ai_suggestions
from users.models import UserProfile

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Bypass CSRF

    def create(self, request, *args, **kwargs):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        user.set_password(password)
        user.save()
        
        # Create user profile with team_name
        team_name = request.data.get('team_name', 'Default Team')
        UserProfile.objects.create(user=user, team_name=team_name)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(ObtainAuthToken):
    authentication_classes = []  # Bypass CSRF
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data
        })

class DashboardStatsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_predictions = DNASequence.objects.filter(user=request.user)
        total = user_predictions.count()
        today_count = user_predictions.filter(created_at__date=timezone.now().date()).count()
        
        class_dist = list(
            user_predictions.values('prediction').annotate(count=Count('id')).order_by('-count')
        )
        
        return Response({
            'total_predictions': total,
            'today_predictions': today_count,
            'class_distribution': class_dist
        })

class ClassifyDNAAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        raw_sequence = request.data.get('sequence', '')
        cleaned = clean_sequence(raw_sequence)
        is_valid, error_msg = validate_sequence(cleaned)

        if not is_valid:
            return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        try:
            predictor = get_predictor()
            result = predictor.predict(cleaned)
            
            ai_explanation = get_ai_explanation(cleaned, result['label'])
            ai_suggestions = get_ai_suggestions(cleaned, result['label'])

            dna_record = DNASequence.objects.create(
                user=request.user,
                sequence=cleaned,
                prediction=result['label'],
                confidence_score=result['confidence'],
                ai_explanation=ai_explanation,
                ai_suggestions=ai_suggestions,
            )
            
            serializer = DNASequenceSerializer(dna_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictionHistoryAPIView(generics.ListAPIView):
    serializer_class = DNASequenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DNASequence.objects.filter(user=self.request.user).order_by('-created_at')
