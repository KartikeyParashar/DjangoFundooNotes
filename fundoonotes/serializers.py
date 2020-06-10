from rest_framework import serializers
from .models import Note, Label


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['collaborator']


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'color']
