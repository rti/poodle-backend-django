from rest_framework import serializers

from .models import Query, Option, Choice, Attendee


class EmbeddedChoiceSerializer(serializers.ModelSerializer):
    attendee = serializers.SlugRelatedField(read_only=True, slug_field='name')
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'attendee', 'attendee_id', 'status']


class EmbeddedOptionSerializer(serializers.ModelSerializer):
    choices = EmbeddedChoiceSerializer(many=True, read_only=True)
    begin_date = serializers.DateField(read_only=True)
    begin_time = serializers.TimeField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    end_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'begin_date', 'begin_time',
                  'end_date', 'end_time', 'choices']


class QuerySerializer(serializers.ModelSerializer):
    options = EmbeddedOptionSerializer(many=True, read_only=True)
    #  choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Query
        fields = ('id', 'name', 'options')
        #  fields = ('id', 'name', 'options', 'choices')


class OptionSerializer(serializers.ModelSerializer):
    query_id = serializers.IntegerField()

    class Meta:
        model = Option
        fields = ['id', 'begin_date', 'begin_time', 'end_date', 'end_time', 'query_id']


class ChoiceSerializer(serializers.ModelSerializer):
    attendee = serializers.SlugRelatedField(read_only=True, slug_field='name')
    attendee_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = Choice
        fields = ['id', 'attendee', 'attendee_id', 'option_id', 'status']


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name']
