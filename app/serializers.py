from rest_framework import serializers

from .models import Query, Option, Choice


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

    def begin_time_short(self):
        return self.begin_time.strftime('%H:%M')

    class Meta:
        model = Option
        fields = ['id', 'begin_date', 'begin_time_short',
                  'end_date', 'end_time_short', 'choices']


class QuerySerializer(serializers.ModelSerializer):
    options = EmbeddedOptionSerializer(many=True, read_only=True)
    #  choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Query
        fields = ('id', 'name', 'options')
        #  fields = ('id', 'name', 'options', 'choices')
