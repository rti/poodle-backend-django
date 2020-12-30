from rest_framework import serializers

from .models import Query, Option, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    attendee = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Choice
        fields = ['id', 'attendee', 'status']


class OptionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    def begin_time_short(self):
        return self.begin_time.strftime('%H:%M')

    class Meta:
        model = Option
        fields = ['id', 'begin_date', 'begin_time_short',
                  'end_date', 'end_time_short', 'choices']


class QuerySerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    #  choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Query
        fields = ('id', 'name', 'options')
        #  fields = ('id', 'name', 'options', 'choices')
