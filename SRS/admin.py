import csv

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# from .resources import AcademicRegistrationResource
from .resources import *

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'middle_name', 'last_name', 'phone', 'sex', 'title', 'is_active',
                    'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('personal', {'fields': ('first_name', 'middle_name', 'last_name', 'sex', 'phone', 'title'),
                      }),

        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups',
                                    'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)


class AcademicEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'rank', 'created_by')
    search_field = ['event', 'rank']
    list_filter = ['event', 'rank']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(AcademicEvent, AcademicEventAdmin)


# class AcademicRegistrationAdmin(ImportExportModelAdmin):
#     list_display = ('student', 'combination','coordinator', 'date')
#     search_field = ['student', ]
#     resource_class = AcademicRegistrationResource
#
#     list_filter = ['coordinator', 'combination']
#
#
# admin.site.register(AcademicRegistration, AcademicRegistrationAdmin)
class CoordinatorAdmin(ImportExportModelAdmin):
    list_display = ('staff', 'rank')
    search_field = ['staff', ]

    list_filter = ['staff', 'rank']


admin.site.register(Coordinator, CoordinatorAdmin)


class WorkLoadAdmin(ImportExportModelAdmin):
    list_display = ('staff', 'subject', 'rank')
    search_field = ['staff', ]

    list_filter = ['staff', 'subject']


admin.site.register(WorkLoad, WorkLoadAdmin)


class AcademicResultAdmin(ImportExportModelAdmin):
    list_display = ('registration', 'event', 'subject', 'marks', 'grade', 'remark')
    search_fields = ['registration']
    list_filter = ['event', 'subject']

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Result, AcademicResultAdmin)


def deactivate_sms_status(modeladmin, request, queryset):
    queryset.update(is_sent=False)


deactivate_sms_status.short_description = 'Deactivate send sms status'


def sms_report(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sms_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['registration ', 'division', 'point', 'is_sent'])
    books = queryset.filter(is_sent=True).values_list('registration', 'division', 'point', 'is_sent')
    for book in books:
        writer.writerow(book)
    return response


sms_report.short_description = 'Export to csv SMS report'


class YearResultAdmin(ImportExportModelAdmin):
    list_display = ('registration', 'event', 'division', 'point', 'weight', 'is_sent')
    search_fields = ['registration__student__entry_number']
    list_filter = ['event', 'is_sent']
    actions = [deactivate_sms_status, sms_report, ]

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(YearResult, YearResultAdmin)


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = (
        'admission', 'entry_number', 'entry_rank', 'first_name', 'middle_name', 'last_name', 'parent_phone', 'sex',
        'entry_date',)
    search_fields = ['entry_number', 'parent_phone']
    list_filter = ['sex']


    # autocomplete_fields = ['district']

    # def save_model(self, request, obj, form, change):
    #     obj.registerer = request.user
    #     obj.save()


admin.site.register(Student, StudentAdmin)


class AcademicYearAdmin(ImportExportModelAdmin):
    list_display = ('financial_year', 'created_by')
    search_fields = ['financial_year', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(AcademicYear, AcademicYearAdmin)


class CombinationAdmin(ImportExportModelAdmin):
    list_display = ('name', 'level', 'created_by')
    search_fields = ['name', ]
    list_filter = ['level']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Combination, CombinationAdmin)


class CombinationSubjectAdmin(ImportExportModelAdmin):
    list_display = ('combination', 'subject', 'created_by')
    search_fields = ['combination', ]
    list_filter = ['combination']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(CombinationSubject, CombinationSubjectAdmin)


class RankAdmin(ImportExportModelAdmin):
    list_display = ('name', 'number', 'level', 'created_by')
    search_fields = ['name', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Rank, RankAdmin)


class LevelAdmin(ImportExportModelAdmin):
    # resource_class = DistrictResource

    list_display = ('name', 'created_by')
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Level, LevelAdmin)


class EventAdmin(ImportExportModelAdmin):
    # resource_class = RegionResource
    list_display = ('name', 'created_by')
    search_fields = ['name', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Event, EventAdmin)


class SubjectAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'is_core', 'created_by')
    search_fields = ['name', ]
    list_filter = ['is_core']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Subject, SubjectAdmin)


# additional models for payments models

class ItemAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'created_by')
    search_fields = ['name', ]

    # list_filter = ['is_core']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Item, ItemAdmin)


class PaymentItemAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('type', 'level', 'amount', 'created_by')
    search_fields = ['type', ]

    list_filter = ['type', 'level']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(PaymentItem, PaymentItemAdmin)


class CharacterAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('code', 'name',)
    search_fields = ['code', ]

    list_filter = ['code', ]


admin.site.register(Character, CharacterAdmin)


class StudentCharacterAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('registration', 'character', 'grade', 'remark')
    search_fields = ['registration', ]

    list_filter = ['registration', ]


admin.site.register(StudentCharacter, StudentCharacterAdmin)


class PaymentTypeAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'account', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Type, PaymentTypeAdmin)


class PaymentStructureAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('level', 'type', 'total', 'minimum')
    search_fields = ['level', ]

    list_filter = ['level', 'level']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(PaymentStructure, PaymentStructureAdmin)


class PaymentAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('registration', 'structure', 'amount', 'due', 'date', 'created_by')
    search_fields = ['registration', ]

    list_filter = ['registration', 'structure']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Payment, PaymentAdmin)


# additional models for registration models

class RegionAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Region, RegionAdmin)


class StatusAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('code', 'created_by')
    search_fields = ['code', ]

    list_filter = ['code']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Status, StatusAdmin)


class DistrictAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'region', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(District, DistrictAdmin)


class SchoolAdmin(ImportExportModelAdmin):
    # resource_class = UnitResource
    list_display = ('name', 'district', 'created_by')
    search_fields = ['name', ]

    list_filter = ['name']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(School, SchoolAdmin)


class RegistrationAdmin(ImportExportModelAdmin):
    resource_class = RegistrationResource
    list_display = ('student', 'academic_year', 'rank', 'status', 'is_active', 'created_by')
    search_fields = ['student', ]

    list_filter = ['student']
    #
    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     obj.save()


admin.site.register(Registration, RegistrationAdmin)
