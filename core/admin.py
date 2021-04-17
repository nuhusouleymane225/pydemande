from django.contrib import admin

from .models import *
from import_export import resources, fields, widgets
# Register your models here.
from import_export.admin import ImportExportModelAdmin


from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import mark_safe
from django.template.defaultfilters import escape


class UserResource(resources.ModelResource):

    class Meta:
        model = UserProfile


class DemandeResource(resources.ModelResource):
    frais_date = fields.Field(attribute='frais_date', column_name='Date', widget=widgets.DateWidget())
    num_releve = fields.Field(attribute='num_releve', column_name="Numéro d'édition")
    chauffeur = fields.Field(attribute='chauffeur', column_name='Chauffeur')
    code_activite = fields.Field(attribute='code_activite', column_name='Code frais')
    montant_ttc = fields.Field(attribute='montant_ttc', column_name='Total', widget=widgets.DecimalWidget())

    class Meta:
        model = Demande
        fields = ('frais_date', 'num_releve', 'chauffeur', 'code_activite', 'montant_ttc')
        export_order = ('frais_date', 'num_releve', 'chauffeur', 'code_activite', 'montant_ttc')
        
         
    def dehydrate_user(self, Demande):
        return '%s' % (Demande.user.username)


    def dehydrate_chauffeur(self, Demande):
        return '%s' % (Demande.chauffeur.code_matricule)

   


class ItemResource(resources.ModelResource):
    view_on_site = False
    class Meta:
        model = Item


class ChauffeurResource(resources.ModelResource):
    view_on_site = False
    class Meta:
        model = Chauffeur


class UserAdmin(ImportExportModelAdmin):
    view_on_site = False
    resource_class = UserResource

class DemandeAdmin(ImportExportModelAdmin):
    view_on_site = False
    list_filter = [
        'demande_date',
        'traite',
        'user',
        'num_releve'
        
        
    ]

    # permettre la recherche dans obj_repr et dans change_message

    search_fields = [
        
        'num_releve',
      
    ]
    resource_class = DemandeResource


class ChauffeurAdmin(ImportExportModelAdmin):
    resource_class = ChauffeurResource

class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource


admin.site.register(Chauffeur, ChauffeurAdmin)
admin.site.register(Demande, DemandeAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Item, ItemAdmin)





@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    #pour avoir un deroulant basé sur l'heure
    date_hierarchy = 'action_time'

    #filtrer le resultat par utilisateur
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # permettre la recherche dans obj_repr et dans change_message

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    
    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
admin.site.site_header = "SUIVI DES FRAIS D'EXPLOITATION"


