from django.db import models


class BotUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True,
                                     unique=True,
                                     null=False,
                                     verbose_name='ID пользователя в Telegram')
    first_name = models.CharField(max_length=20,
                                  null=False,
                                  verbose_name='Имя пользователя в Telegram')
    last_name = models.CharField(max_length=20,
                                 null=True,
                                 verbose_name='Фамилия пользователя в Telegram')

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class MessageBot(models.Model):
    user = models.ForeignKey(to=BotUser, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    media_group = models.BigIntegerField(null=True)
    objects = models.Manager()


class Attachment(models.Model):
    data = models.BinaryField(null=False)
    name = models.CharField(max_length=20,
                            null=False)
    extension = models.CharField(max_length=4,
                                 null=False)
    objects = models.Manager()

    class Meta:
        abstract = True


class AttachmentBot(Attachment):
    message_bot = models.ForeignKey(to=MessageBot,
                                    on_delete=models.CASCADE)


class AttachmentButton(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name='Файлы')

    def __str__(self):
        return self.file.name[8::]

    class Meta:
        verbose_name = 'Файл для кнопок'
        verbose_name_plural = 'Файлы для кнопок'


class Admin(models.Model):
    id = models.BigIntegerField(primary_key=True,
                                unique=True,
                                null=False,
                                verbose_name='ID админинстратора в Telegram')
    firts_name = models.CharField(max_length=20,
                                  null=False,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=20,
                                 null=False,
                                 verbose_name='Фамилия')
    mail = models.CharField(max_length=40,
                            unique=True,
                            null=True,
                            verbose_name='Почта')
    message_on_respond = models.IntegerField(null=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Администраторы'
        verbose_name = 'Администратор'


class Button(models.Model):
    name = models.CharField(max_length=60,
                            verbose_name='Название кнопки')
    callback = models.CharField(max_length=120)
    text = models.TextField(verbose_name='Текст кнопки')
    attachment = models.ManyToManyField(to=AttachmentButton, blank=True,
                                        verbose_name='Файлы')

    class Meta:
        abstract = True


class GrandParentButton(Button):
    class Meta:
        verbose_name_plural = 'Кнопки 1-го уровня'
        verbose_name = 'Кнопка 1-го уровня'

    def __str__(self):
        return f'{self.name}'


class ParentButton(Button):
    grandparent = models.ForeignKey(to=GrandParentButton,
                                    on_delete=models.CASCADE,
                                    verbose_name='Кнопка 1-го уровня',  # отображение к какой кнопке прошлого уровня
                                    # принадлежит эта кнопка
                                    related_name='parent')

    class Meta:
        verbose_name_plural = 'Кнопки 2-го уровня'
        verbose_name = 'Кнопка 2-го уровня'

    def __str__(self):
        return f'{self.name}'


class ChildButton(Button):
    parent = models.ForeignKey(to=ParentButton,
                               on_delete=models.CASCADE,
                               verbose_name='Кнопка 2-го уровня',  # отображение к какой кнопке прошлого уровня
                               # принадлежит эта кнопка
                               related_name='child')

    class Meta:
        verbose_name_plural = 'Кнопки 3-го уровня'
        verbose_name = 'Кнопка 3-го уровня'


class Condition(models.Model):
    user = models.OneToOneField(to=BotUser,
                                on_delete=models.CASCADE)
    creating_message = models.BooleanField(default=False)
