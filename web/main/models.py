from django.db import models


class GroupLesson(models.Model):
    name = models.CharField(verbose_name='название',max_length=100)
    DAY_CHOICES = [
        ('ПН', 'Понедельник'),
        ('ВТ', 'Вторник'),
        ('СР', 'Среда'),
        ('ЧТ', 'Четверг'),
        ('ПТ', 'Пятница'),
    ]
    day = models.CharField(verbose_name='день проведения', max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField(verbose_name='начало')
    end_time = models.TimeField(verbose_name='конец')
    capacity = models.PositiveIntegerField(verbose_name='размер группы')
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def available_slots(self):
        return self.capacity - self.enrollments.count()

    class Meta:
        verbose_name = 'Групповое занятие'
        verbose_name_plural = "Групповые занятия"


class Person(models.Model):
    first_name = models.CharField(verbose_name='имя', max_length=100)
    last_name = models.CharField(verbose_name='фамилия', max_length=100)
    sur_name = models.CharField(verbose_name='отчество', max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(verbose_name='телефон', max_length=20, blank=True, null=True)
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.sur_name}"

    class Meta:
        ordering = ['-created']
        verbose_name = 'Клиент'
        verbose_name_plural = "Клиенты"


class Enrollment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group_lesson = models.ForeignKey(GroupLesson, related_name='enrollments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} записан в {self.group_lesson}"