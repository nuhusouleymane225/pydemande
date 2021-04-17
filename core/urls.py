from django.urls import path
from core.views import (
    Item,
    ItemDetailView,
    MotifView,
    DemandeSummaryView,
    DemandeView,
    add_to_demande,
    remove_from_demande,
    remove_single_item_from_demande,
    demande_traffiche,
    welcome_admin,
    demande_affiche,
    demande_traitement_edit,
    ImprimePdf,
    rapport_mensuel,
    intro,
    delete
)
app_name = 'core'

urlpatterns = [
    path('', intro, name='intro'),
    path('home/', welcome_admin, name='home'),
    path('delete/<int:id>', delete, name='delete'),
    path('demandes/', demande_affiche, name='demandes'), 
    path('demande-summary/', DemandeSummaryView.as_view(), name='demande-summary'),
    path('motifs/', MotifView.as_view(), name='motifs'),
    path('demande/<int:id>', demande_traitement_edit, name='demande'),
    path('motif/<slug>/', ItemDetailView.as_view(), name='motif'),
    path('add-to-demande/<slug>/', add_to_demande, name='add-to-demande'),
    path('remove-from-demande/<slug>/', remove_from_demande, name='remove-from-demande'),
    path('remove-item-from-demande/<slug>/', remove_single_item_from_demande,
         name='remove-single-item-from-demande'),
    path('demandes/traite/', demande_traffiche, name="dtraite"),
    path('demandes/traite/pdf/<int:id>', ImprimePdf, name="pdf_view"), #pdf print
    path('rapport/', rapport_mensuel, name='rapport'),
]
