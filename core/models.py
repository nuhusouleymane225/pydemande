from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.urls import reverse
import qrcode
from io import BytesIO
import random
import string
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.
directionActChoix = [
    ('DGE', 'Dir. Générale(DGE)'),
    ('DCF', 'Dir. Financière(DCF)'),
    ('DRH', 'Dir. RH(DRH)'),
    ('DEX', 'Dir. Exploitation(DEX)'),
    ('DET', 'Dir. Technique(DET)'),
    ('DCM', 'Dir. Commerciale(DCM)'),
    ('SMG', 'Moyens Generaux(SMG)'),
    ('FHY', 'fret Hydrocarbure(FHY)'),
    ('FSB', 'fret boisson(FSB)'),
    ('FHP', 'fret huile de palm(FHP)'),
    ('FTC', 'fret conteneurs(FTC)'),
    ('FCS', 'fret canne à sucre(FCS)'),
    ('FDI', 'fret divers(FDI)'),
    ('LEV', 'levage(LEV)'),
    ('LOC', 'location de surfaces(LOC)'),
    ('SDI', 'services divers(SDI)'),
    ('RAV', 'revenus à ventiler(RAV)'),
    ('PAF', 'Prestation Accessoir(PAF)'),
    ('COL', 'fret Colis lourds(COL)'),

]



codeActivite = [
    ('DGE', 'DGE'),
    ('DCF', 'DCF'),
    ('DRH', 'DRH'),
    ('DEX', 'DEX'),
    ('DET', 'DET'),
    ('DCM', 'DCM'),
    ('SMG', 'SMG'),
    ('FHY', 'FHY'),
    ('FSB', 'FSB'),
    ('FHP', 'FHP'),
    ('FTC', 'FTC'),
    ('FCS', 'FCS'),
    ('FDI', 'FDI'),
    ('LEV', 'LEV'),
    ('LOC', 'LOC'),
    ('SDI', 'SDI'),
    ('RAV', 'RAV'),
    ('PAF', 'PAF'),
    ('COL', 'COL'),

]

axeAnalyseChoix = [
    ('200', 'Batiment et charge locative'),
    ('210', 'Voyage & deplacement'),
    ('220', 'Fourniture & consommable de bureau'),
    ('230', 'Charge personnel'),
    ('240', 'Quote-part depreciation immo'),
    ('250', 'Personnel & services exterieur'),
    ('260', 'Relation exterieur'),
    ('270', 'Impôt & taxes'),
    ('280', 'Autres charges directions et service'),
    ('900', "Recette d'exploitation"),
    ('910', 'Frais/Opération (frais voyages)'),
    ('920', 'Papier administratif-CR'),
    ('930', "Main d'oevre dédiée"),
    ('940', 'Quote-part amortissement CR et autres'),
    ('950', 'Entretien & reparation CR'),
    ('960', 'Frais generaux'),


]


agenceChoix = [
    ('0000', 'Siège'),
    ('0001', 'Abidjan (agence principale)'),
    ('0002', 'Bouaflé'),
    ('0003', 'San-Pedro'),
    ('0007', 'Bouaké'),
    ('0008', 'Yamoussoukro'),
    ('0009', 'Ferké'),
    ('0010', 'Minautores'),


]





class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    direction = models.CharField(max_length=50, choices=directionActChoix)
    code_matricule = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Chauffeur(models.Model):

    nom_prenom = models.CharField(max_length=150, verbose_name='Nom et prénoms')
    code_matricule = models.CharField(max_length=10, verbose_name='Code matricule')
    est_actif = models.BooleanField(default=True, verbose_name='Est Actif')

    class Meta:
        verbose_name = "chauffeur"
        verbose_name_plural = "chauffeurs"

    def __str__(self):
        return f"{self.nom_prenom} - {self.code_matricule}"



class Item(models.Model):
    libelle = models.CharField(max_length=100)
    prix = models.DecimalField(decimal_places=2, max_digits=9999)
    categorie = models.CharField(blank=True, null=True, max_length=255)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.libelle

    def get_absolute_url(self):
        return reverse("core:motif", kwargs={
            'slug': self.slug
        })

    def get_add_to_demande_url(self):
        return reverse("core:add-to-demande", kwargs={
            'slug': self.slug
        })

    def get_remove_from_demande_url(self):
        return reverse("core:remove-from-demande", kwargs={
            'slug': self.slug
        })


class DemandeItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    soumis = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} de  {self.item.libelle}"

    def get_total_item_price(self):
        return self.quantite * self.item.prix



    



import sys
class Demande(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Utilistaeur')
    ref_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Code unique')
    items = models.ManyToManyField(DemandeItem, verbose_name='Motifs')
    demande_date = models.DateTimeField(verbose_name='Date de demande', null=True)
    soumis = models.BooleanField(default=False)
    chauffeur = models.ForeignKey(
        'Chauffeur', related_name='chauffeur', on_delete=models.CASCADE, blank=True, null=True)
    traite = models.BooleanField(default=False, verbose_name='Traité')
    #form fields
    num_releve = models.CharField(
        max_length=20, verbose_name='Numéro de relevé')
    code_vehicule = models.CharField(max_length=50, verbose_name='Code véhicule', blank=True)
    code_remorque = models.CharField(
        max_length=50, verbose_name='Code remorque', blank=True)

    imat_vehicule = models.CharField(
        max_length=50, verbose_name='Imat. véhicule', blank=True)
    imat_remorque = models.CharField(
        max_length=50, verbose_name='Imat. Remorque', blank=True)
    frais_date = models.DateField(verbose_name='Date de frais', null=True)
    montant_ttc = models.DecimalField(decimal_places=2, max_digits=9999, blank=True, null=True)
    # code activite analytique
    code_activite = models.CharField(
        max_length=150, choices=codeActivite, verbose_name='Code Activité')
    libelle_activite = models.CharField(
        max_length=255, choices=directionActChoix, verbose_name='Libelle activité')

    # les autres element de l'analytique
    agence = models.CharField(choices=agenceChoix, max_length=255)
    a_rembourser = models.BooleanField(default=False, verbose_name='A rembourser')
    axe_analyse = models.CharField(choices=axeAnalyseChoix, max_length=255)
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)

    '''
    1. Item added to demande
    2. fill the form
    3. submit the form
    4.receive a notif of process finish
    5. download the document
    
    '''

    def __str__(self):
        return f"{self.user.username}-{self.num_releve}"

    def get_total(self):
        total = 0
        for demande_item in self.items.all():
            total += demande_item.get_total_item_price()
        
        
        return total
    #autogenerated ref from system
    def create_ref_code(self):
        f = ''  
        f.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        return f

    def get_absolute_url(self):
        return reverse('core:demande', args=[str(self.id)])


    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.create_ref_code())
        qr.make(fit=True)

        img = qr.make_image()

        buffer = BytesIO()
        img.save(buffer)
        filename = 'demandes-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', sys.getsizeof(buffer), None)
        self.qrcode.save(filename, filebuffer)


    class Meta:
        ordering = ("-demande_date", "libelle_activite")




def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
