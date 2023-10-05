
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User




class RegisterSerializer(serializers.Serializer):
    username  = serializers.CharField()
    email= serializers.EmailField()
    password= serializers.CharField()    

    def validate(self, data):

        if data['username']:
            if User.objects.filter(username= data['username']).exists():
                raise serializers.ValidationError(' This username is taken')

        if data['email']:
            if User.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError(' This email is taken')

        return data

    def create(sef , validated_data):
        user = User.objects.create(username = validated_data['username'], email= validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

  
        #print (validated_data)
#token omm
# c8d2e33fe6bf623b95badbbe4b03a74043bb9290




class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','color_name']



class PersonSerializer(serializers.ModelSerializer):
    color= ColorSerializer()
    #county = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = '__all__'
        #depth= 1

    # def get_country(self , objs):
    #     color_obj= Color.objects.get(id=obj.color.id)
    #     return {'color_name': color_obj.color_name, 'hex_code':'#000'}

    def validate(self, data):  
        special_characters = "!@#$%^&*()-+_+,<>/"   
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special chars')

    # def validate(self, data):
        
        # if data['age']<18:
        #     raise serializers.ValidationError('age should be greater than 18')
        
        # return data
    
    # def validate_age(self,data):
    #     print(data)
        return data