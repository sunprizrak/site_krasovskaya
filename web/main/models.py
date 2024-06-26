from django.db import models
from users.models import Group


class ScheduleModel(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    time_spending = models.TimeField()
