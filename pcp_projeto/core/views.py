from datetime import date
from django.shortcuts import redirect, render
from .models import Sector, Solicitacao,Ferr_report,Msg_day,Statusos
from .forms import Ferramentaria_form,Ferramentaria_form_report,Status_form
#Imports para gerar pdf.
## Não implementado.
import io
from django.http import FileResponse
import reportlab
from reportlab.pdfgen import canvas

#imports para criar paginação
## Em implementação, necessita criar o filtro.
from django.core.paginator import Paginator, InvalidPage, EmptyPage

#
##
from django.http import HttpResponseRedirect
from django.contrib import messages
import os

#
##Imports para criar MSG dia
##Implementado na index.html
from datetime import datetime

#
##Imports para criar Login/Logout
##Em implementação
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




###############################################

#página de login
def login_user(request):    
    return render(request, 'login.html')

#validação de login
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            usuario = request.user
            grp = request.user.groups.values_list('name',flat = True)
            grp_list = list(grp)
            print('usuário conectado: ',usuario,grp_list)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/login/')

def logout_user(request):
    user = request.user
    print('usuário desconectado: ',user)
    logout(request)   
    return redirect('/')

def teste(request):        
    os_list = Solicitacao.objects.all()    
    # configuração paginação
    p = Paginator(Solicitacao.objects.all(), 3)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    context = {
        'os_list': os_list,
        'ordens': ordens,
        'nums': nums
        }
    return render(request, 'manut_list.html',context)


#página Inicial.
@login_required(login_url='/login/')
def home(request):
    #mensagem do dia, um pequeno motivacional para descontrair.
    msg_date = datetime.today().strftime('%Y-%m-%d')

    try:
        editar = Msg_day.objects.get(current_day=msg_date)
        print(editar)
    except:    
        editar = datetime.today().strftime('%Y-%m-%d')
        print('------------------------------')
        print('Novo acesso homePage')
        print('------------------------------')


    os_list = Solicitacao.objects.all()
    try:
        context = {
            'os_list': os_list,
            'mensagem':editar.mensagem,
        }
    except:
        context = {
        'os_list': os_list,
            'mensagem':'Semear ideias ecológicas e plantar sustentabilidade é ter a garantia de colhermos um futuro fértil e consciente. 🌎'
        }
        
    return render(request, 'index.html',context)

    

#Página de lista de OS, com paginação. Necessita incluir função filtro.
@login_required(login_url='/login/')
def manut_list(request):
    usuario = request.user
    nome = request.user.first_name
    sobrenome = request.user.last_name
    grp = request.user.groups.values_list('id',flat = True)
    print(grp)
    grp_list = list(grp)
    print(usuario, grp_list)
    # Blog.objects.filter(pk__in=[1, 4, 7])
    
    os_list = Solicitacao.objects.all()    
    # configuração paginação
    p = Paginator(Solicitacao.objects.filter(sector__in=grp_list), 50)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    context = {
        'usuario':nome,
        'sobrenome':sobrenome,
        'os_list': os_list,
        'ordens': ordens,
        'nums': nums
        }
    return render(request, 'manut_list.html',context)



#Página do dashboard.
@login_required(login_url='/login/')
def dashboard(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'dashboard.html',context)




@login_required(login_url='/login/')
class ferram_class:
    def ferr_form(request,slug=0):
        if request.method == "GET":
            if slug==0:
                #criar os
                form = Ferramentaria_form()
                return render(request, 'manut_form.html',{'form':form})    
            else:
                try:
                    editar = Solicitacao.objects.get(slug=slug)
                    form = Ferramentaria_form(instance=editar)
                    return render(request, 'manut_form.html',{'form':form})
                except:
                    return redirect('/manut_list/')
        else:
            if slug==0:
                
                form = Ferramentaria_form(request.POST)
                
            else:
                #editar os
                editar = Solicitacao.objects.get(slug=slug)
                form = Ferramentaria_form(request.POST,instance=editar)
                print('atualizado')
            if form.is_valid():
                manut_print = form.save()                
                print('------------------------------')
                user = request.user
                print('Os Criada')
                print('Número da OS: ',manut_print.id,user)                
                #impress_id = manut_print.id
                contexto = {'id':manut_print.id,
                            'fullname':manut_print.fullname,
                            'type_service':manut_print.type_service,
                            'factory':manut_print.factory,
                            'status_os':manut_print.status_os,
                            'machine_code':manut_print.machine_code,
                            'sector':manut_print.sector,
                            'priority_type':manut_print.priority_type,
                            'propose_service':manut_print.propose_service,
                            'issue_desctiption':manut_print.issue_desctiption,
                            'date_create':manut_print.date_create,
                            'hour_arrive':manut_print.hour_arrive,
                            'slug':manut_print.slug,
                            }
                print('------------------------------')
                                          
                return render(request, 'manut_print.html',contexto)


#Em um futuro distante, tentarei renderizar a página através de Query
def manut_impressao(request):    
    
    return render(request, 'manut_print.html')



#Página de detalhe da Os
@login_required(login_url='/login/')
class manut_detail_class:
    def manut_detail(request, slug):
        os_list = Solicitacao.objects.get(slug=slug)
        #print('----------------------')
        #print('Qual é essa os?')
        #print(os_list.id)
        if request.method == "POST":
            form1 = Ferramentaria_form_report(request.POST)
            if form1.is_valid():
                comments = form1.save(commit=False)
                comments.os_number = os_list
                comments.save()
                print('------------------------------')
                print(request.META.get('HTTP_REFERER'))
                print('Atividade de OS Criada')                
                print('OS: ',comments.id)
                print('------------------------------')
                return redirect('manut_detail', slug= os_list.slug)
        else:
            form1 = Ferramentaria_form_report()
        return render(request, 'manut_detail.html', {'os_list':os_list, 'form1':form1})




#Apagar a Ordem de Serviço
@login_required(login_url='/login/')
def form_delete(request, id):
    try:
        os_list = Solicitacao.objects.get(pk=id)
        print('------------------------------')
        print('Atividade de OS deletada')
        print('OS: ',os_list.id)
        print(os_list.fullname,
                os_list.type_service,
                os_list.factory,
                os_list.status_os,
                os_list.machine_code,
                os_list.sector,
                os_list.priority_type,
                os_list.propose_service,
                os_list.issue_desctiption,
                os_list.date_create,
                os_list.hour_arrive,
                os_list.slug,
                )
        print('------------------------------')
        os_list.delete()
        return redirect('/manut_list/')
    except:
        return redirect('/manut_list/')


#Apagar atividades das OS (registros)
@login_required(login_url='/login/')
def apagar_delete(request, id):
    os_number = Ferr_report.objects.get(pk=id)
    print('------------------------------')
    print(request.META.get('HTTP_REFERER'))
    print('OS:',os_number.id)
    print('Atividade de os deletada')
    os_number.delete()
    print('------------------------------')

    messages.add_message(request, messages.INFO, 'Atividade de os deletada.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
    #return redirect('/manut_list/')





#atualizar o status das os.
@login_required(login_url='/login/')
class atualizador_class:
    def updt_close(request, id):
        q = Solicitacao.objects.get(pk=id)
        q.status_os = Statusos.objects.get(pk=2)
        print('alterado status da os:',q.id, 'para >>', q.status_os)
        q.save()
        r_redirect = 'http://192.168.0.153:3306/' + q.slug
        return redirect(r_redirect)

    def updt_open(request, id):
        q = Solicitacao.objects.get(pk=id)
        q.status_os = Statusos.objects.get(pk=1)
        print('alterado status da os:',q.id, 'para >>', q.status_os)
        q.save()
        r_redirect = 'http://192.168.0.153:3306/' + q.slug
        return redirect(r_redirect)


