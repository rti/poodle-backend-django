from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Query(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Queries"


class Option(models.Model):
    begin_date = models.DateField()
    begin_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    def __str__(self):
        result = str(self.begin_date)
        if self.begin_time:
            result += ' ' + str(self.begin_time.strftime('%H:%M'))
        if self.end_date or self.end_time:
            result += ' -'
            if self.end_date:
                result += ' ' + str(self.end_date)
            if self.end_time:
                result += ' ' + str(self.end_time.strftime('%H:%M'))
        return '%s (%s)' % (result, str(self.query))

    class Meta:
        ordering = ['id']


class Attendee(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    YES = 'Y', 'Yes'
    NO = 'N', 'No'
    MAYBE = 'M', 'Maybe'


class Choice(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Status.choices)

    def __str__(self):
        return (self.attendee.name + '\'s choice for "' +
                self.option.query.name + '": ' +
                str(self.option.begin_date) + ' ' + str(self.status) + '')

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=['attendee', 'option'], name='unique_choice')]
