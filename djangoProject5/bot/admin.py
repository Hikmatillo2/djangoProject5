from django.contrib import admin
from .models import *
from .forms import *


#  @admin.register(Condition)
#  class ConditionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'registration', 'on_validate', 'in_main_menu', 'creating_task', 'creating_comment')
#     form = ConditionForm


@admin.register(Admin)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'firts_name', 'last_name', 'mail',)
    form = AdminForm


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name')


@admin.register(GrandParentButton)
class GrandParentButtonAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')
    form = GrandParentForm


@admin.register(ParentButton)
class ParentButtonAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'grandparent_name')
    form = ParentForm

    def grandparent_name(self, parent: ParentButton.objects):
        return parent.grandparent.name

    grandparent_name.short_description = 'Кнопка первого уровня'


@admin.register(ChildButton)
class ChildButtonAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'grandparent_name', 'parent_name')
    form = ChildForm

    def grandparent_name(self, child: ChildButton.objects):
        return child.parent.grandparent.name

    def parent_name(self, child: ChildButton.objects):
        return child.parent.name

    def attachment_name(self, attachment: ChildButton.attachment):
        return ', '.join([attachment.filename for attachment in attachment.all()])

    parent_name.short_description = 'Кнопка второго уровня'
    grandparent_name.short_description = 'Кнопка первого уровня'
    attachment_name.short_description = 'Файлы'


@admin.register(AttachmentButton)
class AttachmentButtonAdmin(admin.ModelAdmin):
    list_display = ('file',)

    
@admin.register(MessageBot)
class AttachmentButtonAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', )
