from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class GroupSchedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.group.name} в {self.day} на {self.start_time} - {self.end_time}"


class Enrollment(models.Model):
    schedule = models.ForeignKey(GroupSchedule, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} enrolled in {self.schedule}"