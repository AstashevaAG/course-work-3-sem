from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export.forms import ExportForm
from import_export.resources import ModelResource
from simple_history.admin import SimpleHistoryAdmin

from .models import Section, Article, Comment


class CommentIsApprovedForm(ExportForm):
    is_approved = forms.BooleanField(
        label='Is Approved',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
    )

class CustomModelAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    pass


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article


class CommentResource(ModelResource):
    class Meta:
        model = Comment
    def __init__(self, **kwargs):
        super().__init__()
        self.is_approved = kwargs.get("is_approved")

    def filter_export(self, queryset, *args, **kwargs):
        return queryset.filter(is_approved=bool(self.is_approved))

    def dehydrate_is_approved(self, comment):
        return 'Yes' if comment.is_approved == 1 else 'No'


class SectionResource(resources.ModelResource):
    class Meta:
        model = Section

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
class ArticleAdmin(ImportExportModelAdmin, CustomModelAdmin):
    resource_class = ArticleResource
    history_list_display = ["content", "section", "created_by"]
    list_display = ('title', 'section', 'created_by_link')
    inlines = [CommentInline]

    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'content'],
        }),
        ('Информация об авторе', {
            'fields': ['created_by'],
            'classes': ['collapse'],
        }),
        ('Информация о разделе', {
            'fields': ['section'],
        }),
    ]

    def created_by_link(self, obj):
        link = reverse('admin:auth_user_change', args=[obj.created_by.id])
        return format_html('<a href="{}">{}</a>', link, obj.created_by.username)

    created_by_link.short_description = 'Created By'

    def get_export_queryset(self, request):
        return Article.objects.filter(comments__isnull=False).distinct()


class CommentAdmin(ImportExportModelAdmin, CustomModelAdmin):
    resource_class = CommentResource
    history_list_display = ["is_approved"]
    export_form_class = CommentIsApprovedForm
    list_display = ['content', 'is_approved', 'article', 'created_by']
    list_filter = ['is_approved', 'created_by']

    def get_export_resource_kwargs(self, request, *args, **kwargs):
        export_form = kwargs["export_form"]
        if export_form:
            return dict(is_approved=export_form.cleaned_data["is_approved"])
        return {}

class SectionAdmin(ExportActionMixin, CustomModelAdmin):
    resource_class = SectionResource


# Register your models here.
admin.site.register(Section, SectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
