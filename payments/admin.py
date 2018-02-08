from django.contrib import admin
from payments.models import (Credit, VerificationInformation,
                             ExtUser, ExtUserManager)
from django.contrib import messages
from django.contrib.auth.models import Group
from payments.forms import CustomUserChangeForm, CustomUserCreationForm


class CreditAdmin(admin.ModelAdmin):

    list_display = ['fo_key', 'approve']
    empty_value_display = '--empty--'

    actions = ['agree']

    def agree(self, request, queryset):
        for i in queryset:
            if i.fo_key.ver_inform_upload and i.fo_key.ver_inform_approve:
                i.approve = True
                i.save()
                self.message_user(request,
                                  message='{} credit approve'.format(i.fo_key))
            else:
                self.message_user(request,
                                  message=messages.error(request,
                                                         '{} credit rejected'.format(i.fo_key))
                                  )


class VerificationInline(admin.StackedInline):
    model = VerificationInformation
    fields = [i.name for i in VerificationInformation._meta.fields]
    verbose_name = 'VerificationInformation'
    verbose_name_plural = 'VerificationInformation'


class UserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    empty_value_display = '--empty--'

    inlines = [
        VerificationInline,
    ]

    list_display = ('email', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = ((None, {'fields': ('email',
                                    'password',
                                    'ver_inform_upload',
                                    'ver_inform_approve'
                                    ),
                         'classes': ('collapses')
                         }),
                 ('Permissions', {'fields':
                                  ('is_superuser',
                                   'is_staff',
                                   'user_permissions')
                                  }),
                 )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    actions = ['take_credit']

    def take_credit(self, request, queryset):
        queryset.update(ver_inform_approve=True)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


admin.site.register(ExtUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Credit, CreditAdmin)
admin.site.register(VerificationInformation)
