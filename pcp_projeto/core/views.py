from datetime import date
from django.shortcuts import redirect, render
from .models import Sector, Solicitacao,Ferr_report,Msg_day,Statusos
from .forms import Ferramentaria_form,Ferramentaria_form_report,Status_form
#Imports para gerar pdf.
## Não implementado.
import io
from django.http import FileResponse


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
            print('------------------------------')
            print('usuário conectado: ',usuario)
            print('------------------------------')
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/login/')

def logout_user(request):
    user = request.user
    print('------------------------------')
    print('usuário desconectado: ',user)
    print('------------------------------')
    logout(request)   
    return redirect('/')

def teste(request):
         
    return render(request, 'advanced.html')
        



def teste_aberto(request):
    usuario = request.user
    sobrenome = request.user.last_name
    grp = request.user.groups.values_list('id',flat = True)
    grp_list = list(grp)
    print('------------------------------')                
    print('Manut Lista')
    print('Usuário: ',usuario)
    msg_date = datetime.today().strftime('%Y-%m-%d')
    try:
        editar = Msg_day.objects.get(current_day=msg_date)
        print(editar)
    except:    
        editar = datetime.today().strftime('%Y-%m-%d')
    print('------------------------------')
    os_list = Solicitacao.objects.all()    
    # configuração paginação

    p = Paginator(Solicitacao.objects.filter(sector__in=grp_list,status_os__in=[1]), 50)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    
    try:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':editar.mensagem,
            }
    except:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':'Semear ideias ecológicas e plantar sustentabilidade é ter a garantia de colhermos um futuro fértil e consciente. 🌎'
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
        usuario = request.user
        print('------------------------------')
        print('Home page:',usuario)
        print('------------------------------')

    os_list = Solicitacao.objects.all()
    usuario = request.user
    try:
        context = {
            'usuario':usuario,
            'os_list': os_list,
            'mensagem':editar.mensagem,
        }
    except:
        context = {
            'usuario':usuario,
            'os_list': os_list,
            'mensagem':'Semear ideias ecológicas e plantar sustentabilidade é ter a garantia de colhermos um futuro fértil e consciente. 🌎'
        }        
    return render(request, 'index.html',context)

    

#Página de lista de OS, com paginação. Necessita incluir função filtro.
@login_required(login_url='/login/')
#Página com todos os itens, sem filtro.
def manut_list(request):
    usuario = request.user
    sobrenome = request.user.last_name
    grp = request.user.groups.values_list('id',flat = True)
    grp_list = list(grp)
    print('------------------------------')                
    print('Manut Lista, página com todos os itens, sem filtro')
    print('Usuário: ',usuario)
    msg_date = datetime.today().strftime('%Y-%m-%d')
    try:
        editar = Msg_day.objects.get(current_day=msg_date)
        print(editar)
    except:    
        editar = datetime.today().strftime('%Y-%m-%d')
    print('------------------------------')
    os_list = Solicitacao.objects.all()    
    # configuração paginação

    p = Paginator(Solicitacao.objects.filter(sector__in=grp_list), 50)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    
    try:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':editar.mensagem,
            }
    except:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':'Semear ideias ecológicas e plantar sustentabilidade é ter a garantia de colhermos um futuro fértil e consciente. 🌎'
            }
                    
    return render(request, 'manut_list.html',context)

@login_required(login_url='/login/')
#Página com todos os itens, com filtro = Status aberto.
def manut_list_aberto(request):
    usuario = request.user
    sobrenome = request.user.last_name
    grp = request.user.groups.values_list('id',flat = True)
    grp_list = list(grp)
    print('------------------------------')              
    print('Manut Lista, página com filtro = Status aberto')
    print('Usuário: ',usuario)
    msg_date = datetime.today().strftime('%Y-%m-%d')
    try:
        editar = Msg_day.objects.get(current_day=msg_date)
        print(editar)
    except:    
        editar = datetime.today().strftime('%Y-%m-%d')
    print('------------------------------')
    os_list = Solicitacao.objects.all()    
    # configuração paginação

    p = Paginator(Solicitacao.objects.filter(sector__in=grp_list,status_os__in=[1]), 50)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    
    try:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':editar.mensagem,
            }
    except:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':'Semear ideias ecológicas e plantar sustentabilidade é ter a garantia de colhermos um futuro fértil e consciente. 🌎'
            }
                    
    return render(request, 'manut_list.html',context)


@login_required(login_url='/login/')
#Página com todos os itens, com filtro = Status fechado.
def manut_list_fechado(request):
    usuario = request.user
    sobrenome = request.user.last_name
    grp = request.user.groups.values_list('id',flat = True)
    grp_list = list(grp)
    print('------------------------------')                
    print('Manut Lista,página com filtro = Status fechado')
    print('Usuário: ',usuario)
    msg_date = datetime.today().strftime('%Y-%m-%d')
    try:
        editar = Msg_day.objects.get(current_day=msg_date)
        print(editar)
    except:    
        editar = datetime.today().strftime('%Y-%m-%d')
    print('------------------------------')
    os_list = Solicitacao.objects.all()    
    # configuração paginação

    p = Paginator(Solicitacao.objects.filter(sector__in=grp_list,status_os__in=[2]), 50)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    
    try:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':editar.mensagem,
            }
    except:    
        context = {
            'usuario':usuario,
            'sobrenome':sobrenome,
            'os_list': os_list,
            'ordens': ordens,
            'nums': nums,
            'mensagem':'Semear ideias ecológicas e plantar sustentabilidade é ter a garantia de colhermos um futuro fértil e consciente. 🌎'
            }
                    
    return render(request, 'manut_list.html',context)











#Página do dashboard.
@login_required(login_url='/login/')
def dashboard(request):
    usuario = request.user
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list,
        'usuario':usuario
    }
    return render(request, 'dashboard.html',context)




@login_required(login_url='/login/')
class ferram_class:
    @login_required(login_url='/login/')
    def ferr_form(request,slug=0):
        usuario = request.user        
        if request.method == "GET":
            if slug==0:
                #criar os
                form = Ferramentaria_form()
                return render(request, 'manut_form.html',{'form':form,'usuario':usuario})    
            else:
                try:
                    editar = Solicitacao.objects.get(slug=slug)
                    form = Ferramentaria_form(instance=editar)
                    return render(request, 'manut_form.html',{'form':form,'usuario':usuario})
                except:
                    return redirect('/manut_list/')
        else:
            if slug==0:                
                form = Ferramentaria_form(request.POST)                
            else:
                #editar os
                editar = Solicitacao.objects.get(slug=slug)
                form = Ferramentaria_form(request.POST,instance=editar)
                print('Atualizou OS')
            if form.is_valid():
                manut_print = form.save()     
                user = request.user           
                print('------------------------------')                
                print('Os Criada')
                print('Número da OS: ',manut_print.id,user)
                print('------------------------------')              
                #impress_id = manut_print.id
                usuario = request.user                
                contexto = {'usuario':usuario,
                            'id':manut_print.id,
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
                return render(request, 'manut_print.html',contexto)


#Em um futuro distante, tentarei renderizar a página através de Query
def manut_impressao(request):    
    
    return render(request, 'manut_print.html')



#Página de detalhe da Os
@login_required(login_url='/login/')
class manut_detail_class:
    @login_required(login_url='/login/')
    def manut_detail(request, slug):
        usuario = request.user
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
                print('OS: ',comments.id,usuario)
                print('------------------------------')
                return redirect('manut_detail', slug= os_list.slug)
        else:
            form1 = Ferramentaria_form_report()
        return render(request, 'manut_detail.html', {'os_list':os_list, 'form1':form1,'usuario':usuario })




#Apagar a Ordem de Serviço
@login_required(login_url='/login/')
def form_delete(request, id):
    try:
        os_list = Solicitacao.objects.get(pk=id)
        usuario = request.user
        print('------------------------------')
        print('Formulario deletado')
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
        print('Quem deletou: ', usuario)
        print('------------------------------')
        os_list.delete()
        return redirect('/manut_list/')
    except:
        return redirect('/manut_list/')


#Apagar atividades das OS (registros)
@login_required(login_url='/login/')
def apagar_delete(request, id):
    os_number = Ferr_report.objects.get(pk=id)
    usuario = request.user
    print('------------------------------')
    print(request.META.get('HTTP_REFERER'))
    print('Histórico da ordem de serviço')
    print('Quem deletou: ', usuario)
    print('OS:',os_number.id)    
    os_number.delete()
    print('------------------------------')

    messages.add_message(request, messages.INFO, 'Atividade de os deletada.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
    #return redirect('/manut_list/')





#atualizar o status das os.
@login_required(login_url='/login/')
class atualizador_class:
    @login_required(login_url='/login/')
    def updt_close(request, id):
        usuario = request.user
        q = Solicitacao.objects.get(pk=id)
        q.status_os = Statusos.objects.get(pk=2)
        print('------------------------------')
        print('alterado status da os:',q.id, '\n para >>', q.status_os)
        print('Quem fez: ',usuario)
        print('------------------------------')
        q.save()
        r_redirect = 'http://192.168.0.153:3306/' + q.slug
        return redirect(r_redirect)

    @login_required(login_url='/login/')
    def updt_open(request, id):
        usuario = request.user
        q = Solicitacao.objects.get(pk=id)
        q.status_os = Statusos.objects.get(pk=1)
        print('------------------------------')
        print('alterado status da os:',q.id, '\n para >>', q.status_os)
        print('Quem fez: ',usuario)
        print('------------------------------')
        q.save()
        r_redirect = 'http://192.168.0.153:3306/' + q.slug
        return redirect(r_redirect)


