from django.db import models


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
    query = models.ForeignKey(
            Query, related_name='options', on_delete=models.CASCADE)

    def time_str(time):
        if time:
            return time.strftime('%H:%M')
        return None

    def begin_time_short(self):
        return Option.time_str(self.begin_time)

    def end_time_short(self):
        return Option.time_str(self.end_time)

    # TODO: appending the Query name here is only required to identify
    # Options in the admin form. Find a way to only append the Query name there
    def __str__(self):
        result = str(self.begin_date)
        if self.begin_time:
            result += ' ' + str(self.begin_time_short())
        if self.end_date or self.end_time:
            result += ' -'
            if self.end_date:
                result += ' ' + str(self.end_date)
            if self.end_time:
                result += ' ' + str(self.end_time_short())
        return '%s (%s)' % (result, str(self.query))


class Attendee(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    YES = 'Y', 'Yes'
    NO = 'N', 'No'
    MAYBE = 'M', 'Maybe'


class Choice(models.Model):
    attendee = models.ForeignKey(
            Attendee, related_name='choices', on_delete=models.CASCADE)
    option = models.ForeignKey(
            Option, related_name='choices', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Status.choices)

    def __str__(self):
        return (self.attendee.name + '\'s choice for "' +
                self.option.query.name + '": ' +
                str(self.option.begin_date) + ' ' + str(self.status) + '')

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=['attendee', 'option'], name='unique_choice')]
