from rest_framework import serializers
from entry.models import EntryModels

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryModels
        fields = ['name','title','description','submission','competition']
        
    def create(self, validated_data):
        entry = EntryModels(**validated_data)
        breakpoint()
        entry.created_by = entry.user.id
        entry.save()
        return entry

    def update(self,instance,validated_data):
        request = self.context.get('request')
        user = request.user
        instance.name=validated_data.get('name',instance.name)
        instance.title=validated_data.get('title',instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.submission= validated_data.get('submission',instance.submission)
        instance.user = validated_data.get('user',user)
        instance.competition = validated_data.get('competition',instance.competition)
        instance.updated_by = user.id
        instance.save()
        return instance            