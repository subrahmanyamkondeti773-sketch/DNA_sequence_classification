from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DNASequence
from users.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['team_name', 'bio', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class DNASequenceSerializer(serializers.ModelSerializer):
    confidence_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = DNASequence
        fields = [
            'id', 'sequence', 'prediction', 'confidence_score', 
            'confidence_percent', 'ai_explanation', 'ai_suggestions', 'created_at'
        ]
        read_only_fields = ['prediction', 'confidence_score', 'ai_explanation', 'ai_suggestions', 'created_at']
