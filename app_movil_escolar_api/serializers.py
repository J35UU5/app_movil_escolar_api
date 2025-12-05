from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
import json

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    fecha_nacimiento = serializers.SerializerMethodField()

    def get_fecha_nacimiento(self, obj):
        val = getattr(obj, 'fecha_nacimiento', None)
        if val is None:
            return None
        # Si es datetime o date -> devolver ISO date (YYYY-MM-DD)
        try:
            return val.date().isoformat() if hasattr(val, 'date') else str(val)
        except Exception:
            return str(val)
        
    class Meta:
        model = Alumnos
        fields = '__all__'

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    fecha_nacimiento = serializers.SerializerMethodField()

    def get_fecha_nacimiento(self, obj):
        val = getattr(obj, 'fecha_nacimiento', None)
        if val is None:
            return None
        # Si es datetime o date -> devolver ISO date (YYYY-MM-DD)
        try:
            return val.date().isoformat() if hasattr(val, 'date') else str(val)
        except Exception:
            return str(val)
        
    class Meta:
        model = Maestros
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Parsear materias_json cuando se devuelve
        if data.get('materias_json'):
            try:
                data['materias_json'] = json.loads(data['materias_json'])
            except (json.JSONDecodeError, TypeError):
                data['materias_json'] = []
        else:
            data['materias_json'] = []
        return data

class EventoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventosAcademicos
        fields = '__all__'