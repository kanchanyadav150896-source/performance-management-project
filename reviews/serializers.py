from rest_framework import serializers
from .models import Review, Score, ReviewCycle

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Score must be 1-10")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True, required=False)
    
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        scores_data = validated_data.pop('scores', [])
        review = Review.objects.create(**validated_data)
        for score in scores_data:
            Score.objects.create(review=review, **score)
        return review

class ReviewCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCycle
        fields = '__all__'
