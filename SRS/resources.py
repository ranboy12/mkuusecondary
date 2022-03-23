from import_export import resources, fields

from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User
from import_export.widgets import ForeignKeyWidget

from .models import *


#
#
class StudentResource(resources.ModelResource):
    entry_rank = fields.Field(
        column_name='entry_rank',
        attribute='entry_rank',
        widget=ForeignKeyWidget(Rank, 'number')

    )

    # combination = fields.Field(
    #     column_name='combination',
    #     attribute='combination',
    #     widget=ForeignKeyWidget(Combination, 'name')
    #
    # )

    class Meta:
        model = Student
        fields = (
            'id', 'admission', 'first_name', 'middle_name', 'last_name', 'parent_phone', 'sex', 'entry_rank')


class RegistrationResource(resources.ModelResource):
    rank = fields.Field(
        column_name='rank',
        attribute='rank',
        widget=ForeignKeyWidget(Rank, 'number')

    )

    combination = fields.Field(
        column_name='combination',
        attribute='combination',
        widget=ForeignKeyWidget(Combination, 'name')

    )
    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=ForeignKeyWidget(Status, 'code')

    )
    academic_year = fields.Field(
        column_name='academic_year',
        attribute='academic_year',
        widget=ForeignKeyWidget(AcademicYear, 'financial_year')

    )

    class Meta:
        model = Registration
        fields = (
            'id', 'student', 'rank', 'combination', 'is_registered', 'is_active', 'status', 'academic_year')


#
# class DistrictResource(resources.ModelResource):
#     subject = fields.Field(
#         column_name='subject',
#         attribute='subject',
#         widget=ForeignKeyWidget(Subject, 'name')
#
#     )
#     combination = fields.Field(
#         column_name='combination',
#         attribute='combination',
#         widget=ForeignKeyWidget(Combination, 'name')
#
#     )
#
#     class Meta:
#         model = CombinationSubject
#         fields = ('id', 'combination', 'subject')
#
#
from import_export import resources


# class StudentResource(resources.ModelResource):
#     registerer = fields.Field(
#         column_name='registerer',
#         attribute='registerer',
#         widget=ForeignKeyWidget(User, 'email')
#
#     )
#
#     class Meta:
#         model = Student
#         fields = ('id', 'first_name', 'middle_name', 'last_name', 'parent_phone', 'sex', 'registerer')
# #
#
# class OrganizationResource(resources.ModelResource):
#     class Meta:
#         model = Region
#         fields = ('id', 'name', 'email')
#
#
# class UnitResource(resources.ModelResource):
#     class Meta:
#         model = Unit
#         fields = ('id', 'name', 'abb',)
#
#
# class DepartmentResource(resources.ModelResource):
#     unit = fields.Field(
#         column_name='unit',
#         attribute='unit',
#         widget=ForeignKeyWidget(Unit, 'abb')
#
#     )
#
#     class Meta:
#         model = Department
#         fields = ('id', 'name', 'abb', 'unit')
#
#
class RegionResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')

    )

    class Meta:
        model = Region
        fields = ('id', 'name', 'created_by')


class DistrictResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')

    )
    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ForeignKeyWidget(Region, 'name')

    )

    class Meta:
        model = District
        fields = ('id', 'name', 'created_by')
