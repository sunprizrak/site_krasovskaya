from ckeditor.fields import RichTextField
from django.db import models


class GroupLesson(models.Model):
    name = models.CharField(verbose_name='название',max_length=100)
    description = RichTextField(verbose_name='Описание', default='')
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
    city = models.CharField(verbose_name='город проведения', default='неизвестен')
    price = models.IntegerField(verbose_name='Цена', default=0)
    show_if_no_seats = models.BooleanField(default=False, verbose_name='отображать, если нет мест')
    CURRENCY_CHOICES = [
        ('$', 'USD'),
        ('€', 'EUR'),
        ('₽', 'RUB'),
        ('Br', 'BYN')
    ]
    currency = models.CharField(verbose_name='Валюта', max_length=3, choices=CURRENCY_CHOICES, default='€')
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def available_slots(self):
        return self.capacity - self.enrollments.count()

    @property
    def get_price(self):
        return f"{self.price}{self.currency}"

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

    @property
    def enrolled_groups(self):
        return ", ".join([str(enrollment.group_lesson) for enrollment in self.enrollment_set.all()])

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


class Question(models.Model):
    name = models.CharField(verbose_name='имя',max_length=100)
    contact = models.CharField(verbose_name='контактные данные', max_length=100)
    text = models.TextField(verbose_name='текст')
    agree_to_privacy_policy = models.BooleanField(
        default=False,
        verbose_name='согласен на обработку персональных данных'
    )
    is_read = models.BooleanField(default=False, verbose_name='прочитано')
    created = models.DateTimeField(verbose_name='получен', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class WantWriteGroup(models.Model):
    name = models.CharField(verbose_name='имя', max_length=100)
    contact = models.CharField(verbose_name='контактные данные', max_length=100)
    group = models.ForeignKey(
        GroupLesson,
        verbose_name='группа',
        on_delete=models.CASCADE,
    )
    agree_to_privacy_policy = models.BooleanField(
        default=False,
        verbose_name='согласен на обработку персональных данных'
    )
    is_read = models.BooleanField(default=False, verbose_name='прочитано')
    created = models.DateTimeField(verbose_name='получен', auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created']
        verbose_name = 'Желающий записаться в группу'
        verbose_name_plural = "Желающие записаться в группу"