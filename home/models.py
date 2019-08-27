from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Person(models.Model):
    cheks = models.BooleanField(default=False)
    title = 'cheks'
    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор:')
    compania = models.TextField(verbose_name='Организации:', default='')
    inn = models.IntegerField(verbose_name='ИНН:', default='')
    kpp = models.IntegerField(verbose_name='КПП:', default='')
    phone = models.IntegerField(verbose_name='Телефон:', default='')
    title = models.TextField(max_length=500, verbose_name='Заголовок:')
    text = models.TextField(max_length=1000, verbose_name='Описание:')
    cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='Стоимость:')
    que = models.IntegerField(verbose_name='Колличество(Укажите 0 если не нужна такая инофрмация):', default='')
    region = models.CharField(verbose_name='Регион закупки:', max_length=100)
    supply = models.CharField(verbose_name='Место поставки ', max_length=100)
    start = models.DateField(verbose_name='Дата размещения:')
    ending = models.DateField(verbose_name='Окончание приёма предложений:')
    nameFile = models.FileField(verbose_name="Документы:")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тендер"
        verbose_name_plural = "Тендер"

class GoTender(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор:')
    tenders = models.ForeignKey(Post, models.SET_NULL, blank=True, null=True,
                                verbose_name="Тендер:")
    cash = models.IntegerField(verbose_name="Сумма:")
    ques = models.IntegerField(verbose_name="Колличество:",default='')
    phones = models.IntegerField(verbose_name='Телефон:', default='')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    prov = True

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cash)

    class Meta:
        verbose_name = "Вступительная сумма"
        verbose_name_plural = "Вступительная сумма"

class BuyTender(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор:')
    tenders = models.ForeignKey(Post, models.SET_NULL, blank=True, null=True,
                                verbose_name="Тендер")
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='owner')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return 'Покупатель - ' + str(self.client) + '  |  Тендер - ' + str(self.tenders)

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупка"