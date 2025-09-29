from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

    def validate_progress(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Progress must be 0-100")
        return value
