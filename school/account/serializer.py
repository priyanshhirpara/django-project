from rest_framework import serializers
from account.models import CustomUser



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'birthdate', 'email', 'password', 'role']
    def create(self, validated_data): 
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user.created_by = user.id
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.birthdate = validated_data.get('birthdate',instance.birthdate)
        instance.email = validated_data.get('email',instance.email)
        instance.set_password(validated_data['password'])
        instance.role = validated_data.get('role',instance.role)
        instance.updated_by = validated_data.get('id',instance.id)
        instance.save()
        return instance
    
class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email','password']

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','birthdate','email','role']
