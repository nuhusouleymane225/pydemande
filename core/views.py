from django.http import request
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout_then_login



from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse, request
from django.template.loader import get_template
from .forms import DemandeForm, DemandeTraitementForm
from .models import (
    Item, Demande, Chauffeur, DemandeItem, UserProfile
)
#fusionchart
from .fusioncharts import FusionCharts
# Create your views here.
from qr_code.qrcode.utils import QRCodeOptions

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

@login_required
def ImprimePdf(request, id):
    texts = Demande.objects.get(id=id)
    
    context = {
        'texts': texts,
        'qrcode': QRCodeOptions(size='t', border=6, error_correction='L'),
    }

    return render_to_pdf('pdf_template.html', context)




def login(request):
    template_name='login.html'
    return render(request , template_name )


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        template_name='index.html'
        login(request, user)
        return render(request,template_name)
    else:
        print('login none ')
        return 0

def logout_view(request):
    logout(request)
    template_name='login.html'
    return render(request, template_name)



def logoutTlogin(request):
    return logout_then_login(request, login_url='/login')



@login_required
def demande_traitement_edit(request, id):
    result= Demande.objects.get(id=id, soumis=False)
    form = DemandeTraitementForm(initial={'items': result.items.all(), 'user': request.user, 'frais_date': result.frais_date, 'code_activite': result.user.userprofile.direction, 'libelle_activite': result.user.userprofile.direction, 'montant_ttc': result.get_total})
    if request.method == "POST":
        form = DemandeTraitementForm(request.POST, instance=result)
        if form.is_valid():
            try:
                form.instance.soumis = True
                form.instance.montant_ttc = form.instance.get_total()
                form.instance.ref_code = form.instance.create_ref_code()
                form.instance.demande_date = timezone.now()
                form.save()
                messages.info(request, "Votre demande a été soumise avec succès merci de patienter durant la validation.")
                return redirect('/home')
            except Exception as e:
                print(e)
                messages.warning(request, "Une erreur s'est produite veuillez rééssayer!")
                return redirect("core:motifs")
    context = {'form': form, 'result':result}
    return render(request,'demande.html',context)  

@login_required
def delete(request, id):
    
    obj =  get_object_or_404(Demande, id=id)
    if obj:
        obj.delete()
        messages.success(request, "Votre demande a été annulée !")
        return redirect("/home")
    else:
        messages.warning(request, "Vous n'avez pas de demande en cours")
        return redirect("/home")



@login_required
def rapport_mensuel(request):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = { 
        "caption": "Montant par Code activité",
            "subCaption": "",
            "xAxisName": "Code activité",
            "yAxisName": "Montant (en XOF)",
            "numberPrefix": "",
            "theme": "umber"
        }
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list
    for key in Demande.objects.all():
        data={}
        data['label'] = key.libelle_activite
        data['value'] = float(key.get_total())
        dataSource['data'].append(data)
    # Create an object for the Column 2D chart using the FusionCharts class constructor 
    template_name='charts.html'
    column2D = FusionCharts("column2D", "ex1" , "900", "350", "chart-1", "json", dataSource)
    return render(request , template_name, {'output': column2D.render()} )




@login_required
def motifs(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "motifs.html", context)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def intro(request):
    template_name = 'home.html'
    return render(request, template_name)

@login_required
def welcome_admin(request):
    template_name='index.html'
    nb_dmd=Demande.objects.all().filter(traite=False).count()
    nb_dmdt=Demande.objects.all().filter(traite=True).count()
    nb_dmds=Demande.objects.all().filter(soumis=False, traite=False).count()
    

    context = {'nb_dmd': nb_dmd, 'nb_dmdt': nb_dmdt, 'nb_dmds': nb_dmds}
    return render(request , template_name, context )


@login_required
def demande_affiche(request):
    query_results=Demande.objects.all().filter(traite=False)
    template_name='tables2.html'
    context={"query_results":query_results}
    return render(request , template_name ,context)


@login_required
def demande_traffiche(request):
    query_results=Demande.objects.all().filter(traite=True)
    template_name='tables2.html'
    context={"query_results":query_results}
    return render(request , template_name ,context)


class DemandeView(View):
    def get(self, *args, **kwargs):
        try:
            demande = Demande.objects.get(user=self.request.user, soumis=False)
            form = DemandeForm(initial={'user': self.request.user, 'items': demande.items.all(), 'code_activite': demande.user.userprofile.direction})
            context = {
                'form': form,
                'demande': demande,
            }
            print(str(self.request.user))
            print("get sucess")
            return render(self.request, "demande.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Vous n'avez pas de demande non soumise")
            return redirect("core:demande")

    def post(self, *args, **kwargs):
        form = DemandeForm(self.request.POST or None)
        try:
            demande = Demande.objects.filter(user=self.request.user, soumis=False)
            
            if form.is_valid():
                for item in demande:
                    
                    item.save()
                    
                demande.soumis = True
                demande.save()                                                                                                                                                ()
                print("post succes")
               
                messages.success(self.request, "Votre demande a été soumise avec succès!")
                return redirect("/")
            else:
                print("error")
                messages.info(self.request, "veuillez vérifier les informations entrées")
        except ObjectDoesNotExist:
            messages.info(self.request, "Vous n'avez pas de demande non soumise")
            return redirect("core:demande-summary")


class MotifView(LoginRequiredMixin, ListView):
    model = Item
    paginate_by = 10
    template_name = "motifs.html"



class DemandeSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            demande = Demande.objects.get(user=self.request.user, soumis=False)
            context = {
                'object': demande
            }
            return render(self.request, 'demande_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Vous n'avez pas de demande non soumise")
            return redirect("/home")




class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "motif.html"

@login_required
def add_to_demande(request, slug):
    item = get_object_or_404(Item, slug=slug)
    demande_item, created = DemandeItem.objects.get_or_create(
        item=item,
        user=request.user,
        soumis=False
    )
    demande_qs = Demande.objects.filter(user=request.user, soumis=False)
    if demande_qs.exists():
        demande = demande_qs[0]
        # check if the order item is in the order
        if demande.items.filter(item__slug=item.slug).exists():
            demande_item.quantite += 1
            demande_item.save()
            messages.info(request, "La  quantite du motif a été mise à jour.")
            return redirect("core:demande-summary")
        else:
            demande.items.add(demande_item)
            messages.info(request, "Ce motif a été  ajouté avec succès à votre demande.")
            return redirect("core:demande-summary")
    else:
        demande_date = timezone.now()
        demande = Demande.objects.create(
            user=request.user, demande_date=demande_date)
        demande.items.add(demande_item)
        messages.info(request, "Ce motif a été ajouté avec succès à votre demande.")
        return redirect("core:demande-summary")


@login_required
def remove_from_demande(request, slug):
    item = get_object_or_404(Item, slug=slug)
    demande_qs = Demande.objects.filter(
        user=request.user,
        soumis=False
    )
    if demande_qs.exists():
        demande = demande_qs[0]
        # check if the demande item is in the demande
        if demande.items.filter(item__slug=item.slug).exists():
            demande_item = DemandeItem.objects.filter(
                item=item,
                user=request.user,
                soumis=False
            )[0]
            demande.items.remove(demande_item)
            demande_item.delete()
            messages.info(request, "Ce motif a été supprimé avec succès à votre demande.")
            return redirect("core:demande-summary")
        else:
            messages.info(request, "Ce motif n'était pas dans votre demande")
            return redirect("core:motif", slug=slug)
    else:
        messages.info(request, "Vous n'avez pas de demande non soumise")
        return redirect("core:motif", slug=slug)


@login_required
def remove_single_item_from_demande(request, slug):
    item = get_object_or_404(Item, slug=slug)
    demande_qs = Demande.objects.filter(
        user=request.user,
        soumis=False
    )
    if demande_qs.exists():
        demande = demande_qs[0]
        # check if the order item is in the order
        if demande.items.filter(item__slug=item.slug).exists():
            demande_item = DemandeItem.objects.filter(
                item=item,
                user=request.user,
                soumis=False
            )[0]
            if demande_item.quantite > 1:
                demande_item.quantite -= 1
                demande_item.save()
            else:
                demande.items.remove(demande_item)
            messages.info(request, "La  quantite du motif a été mise à jour.")
            return redirect("core:demande-summary")
        else:
            messages.info(request, "Ce motif n'était pas dans votre demande")
            return redirect("core:motif", slug=slug)
    else:
        messages.info(request, "Vous n'avez pas de demande non soumise")
        return redirect("core:demande", slug=slug)
