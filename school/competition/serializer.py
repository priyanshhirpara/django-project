from rest_framework import serializers
from competition.models import CompetitionModels

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionModels
        fields = ['name','description','start_date','end_date','prize']

    def create(self, validated_data):
        competition = CompetitionModels(**validated_data)
        competition.created_by = competition.user.id
        competition.save()
        return competition
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.start_date = validated_data.get('start_date',instance.start_date)
        instance.end_date = validated_data.get('end_date',instance.end_date)
        instance.prize = validated_data.get('prize',instance.prize)
        instance.user = validated_data.get('user',user)
        instance.updated_by = validated_data.get('id',user.id)
        instance.save()
        return instance