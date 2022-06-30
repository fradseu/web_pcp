### Projeto PCP-WEB
##
# Horas gastas até o momento = 416h,
# Início do projeto 07/04/2022 >>> 22/06/2022,
# Objetivo do projeto já foi alcançado, 
# 

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

from django.views.generic import TemplateView
from django.db.models import Count



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

         
    return render(request, 'chartjs.html')
        



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
    current_time = datetime.now()
    usuario = request.user
    os_list = Solicitacao.objects.all()
    
    #mes = date.month()
    #ano = date.year()
    
    #print(mes)
    #print(ano)

    labels = []
    data = []
    maior = Solicitacao.objects.order_by('-factory')[:5]
    menor = Solicitacao.objects.order_by('factory')[:5]
        
    
    # ###testes de filtros para plotar o dashboard

    # #Filtro Geral da fábrica MFX
    # mfx_geral = Solicitacao.objects.filter(factory__in=[2]).count()
    # #biblioteca 
    # #print('MFX: ',mfx_geral)
    # #Filtro Mês Atual da fábrica MFX
    # mfx_m = Solicitacao.objects.filter(factory__in=[2],date_create__month=current_time.month).count()
    # #print('mes', mfx_m)

    #  #Filtro Geral da fábrica SPD
    # spdb_geral = Solicitacao.objects.filter(factory__in=[3]).count()
    # #print('SPD: ',spdb_geral)
    # #Filtro Mês Atual da fábrica MFX
    # spd_m = Solicitacao.objects.filter(factory__in=[3],date_create__month=current_time.month).count()



# RANKING DE FÁBRICAS QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES (GERAL)

    donut2 = Solicitacao.objects.values_list('factory__title').annotate(qtd_count=Count('factory')).order_by('-qtd_count')[:10]
    #print('fabricas',fabricas)
    #print('mes', spd_m)

    #RANKING 0
    fabrica0_g = donut2[0]
    #print('setor0', setor0_)
    fabrica0_nome_g = fabrica0_g[0]
    fabrica0_valor_g = fabrica0_g[1]

    #RANKING 0
    fabrica1_g = donut2[1]
    #print('setor0', setor0_)
    fabrica1_nome_g= fabrica1_g[0]
    fabrica1_valor_g = fabrica1_g[1]




# RANKING DE FÁBRICAS QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES (Mês atual)

    donut1 = Solicitacao.objects.filter(date_create__month=current_time.month).values_list('factory__title').annotate(qtd_count=Count('factory')).order_by('-qtd_count')[:10]
    #print('fabricas',fabricas)
    #print('mes', spd_m)

    #RANKING 0
    fabrica0_ = donut1[0]
    #print('setor0', setor0_)
    fabrica0_nome = fabrica0_[0]
    fabrica0_valor = fabrica0_[1]

    #RANKING 0
    fabrica1_ = donut1[1]
    #print('setor0', setor0_)
    fabrica1_nome = fabrica1_[0]
    fabrica1_valor = fabrica1_[1]



# RANKING DE SETORES QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES

    barras1 = Solicitacao.objects.values_list('sector__title').annotate(qtd_count=Count('sector')).order_by('-qtd_count')[:10]
    #print(barras1)
    #elemento2 = barras1[0]

    #RANKING 0
    setor0_ = barras1[0]
    #print('setor0', setor0_)
    setor0_nome = setor0_[0]
    setor0_valor = setor0_[1]

    #RANKING 1
    setor1_ = barras1[1]
    #print('setor1', setor1_)
    setor1_nome = setor1_[0]
    setor1_valor = setor1_[1]

    #RANKING 2
    setor2_ = barras1[2]
    #print('setor2', setor1_)
    setor2_nome = setor2_[0]
    setor2_valor = setor2_[1]

    #RANKING 3
    setor3_ = barras1[3]
    #print('setor3', setor1_)
    setor3_nome = setor3_[0]
    setor3_valor = setor3_[1]

    #RANKING 4
    setor4_ = barras1[4]
    #print('setor4', setor4_)
    setor4_nome = setor4_[0]
    setor4_valor = setor4_[1]

    #RANKING 5
    setor5_ = barras1[5]
    #print('setor5', setor5_)
    setor5_nome = setor5_[0]
    setor5_valor = setor5_[1]

    #RANKING 6
    setor6_ = barras1[6]
    #print('setor6', setor6_)
    setor6_nome = setor6_[0]
    setor6_valor = setor6_[1]

    #RANKING 7
    setor7_ = barras1[7]
    #print('setor7', setor7_)
    setor7_nome = setor7_[0]
    setor7_valor = setor7_[1]

    #RANKING 8
    setor8_ = barras1[8]
    #print('setor8', setor8_)
    setor8_nome = setor8_[0]
    setor8_valor = setor8_[1]

    #RANKING 9
    setor9_ = barras1[9]
    #print('setor9', setor1_)
    setor9_nome = setor9_[0]
    setor9_valor = setor9_[1]



# RANKING DE SETORES QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES (Mês atual)

    barras2 = Solicitacao.objects.filter(date_create__month=current_time.month).values_list('sector__title').annotate(qtd_count=Count('sector')).order_by('-qtd_count')[:10]
    #print(barras1)
    #elemento2 = barras1[0]

    #RANKING 0
    setor0_g = barras2[0]
    #print('setor0', setor0_)
    setor0_nome_g = setor0_g[0]
    setor0_valor_g = setor0_g[1]

    #RANKING 1
    setor1_g = barras2[1]
    #print('setor1', setor1_)
    setor1_nome_g = setor1_g[0]
    setor1_valor_g = setor1_g[1]

    #RANKING 2
    setor2_g = barras2[2]
    #print('setor2', setor1_)
    setor2_nome_g = setor2_g[0]
    setor2_valor_g = setor2_g[1]

    #RANKING 3
    setor3_g = barras2[3]
    #print('setor3', setor1_)
    setor3_nome_g = setor3_g[0]
    setor3_valor_g = setor3_g[1]

    #RANKING 4
    setor4_g = barras2[4]
    #print('setor4', setor4_)
    setor4_nome_g = setor4_g[0]
    setor4_valor_g = setor4_g[1]

    #RANKING 5
    setor5_g = barras2[5]
    #print('setor5', setor5_)
    setor5_nome_g = setor5_g[0]
    setor5_valor_g = setor5_g[1]

    #RANKING 6
    setor6_g = barras2[6]
    #print('setor6', setor6_)
    setor6_nome_g = setor6_g[0]
    setor6_valor_g = setor6_g[1]

    #RANKING 7
    setor7_g = barras2[7]
    #print('setor7', setor7_)
    setor7_nome_g = setor7_g[0]
    setor7_valor_g = setor7_g[1]

    #RANKING 8
    setor8_g = barras2[8]
    #print('setor8', setor8_)
    setor8_nome_g = setor8_g[0]
    setor8_valor_g = setor8_g[1]

    #RANKING 9
    setor9_g = barras2[9]
    #print('setor9', setor1_)
    setor9_nome_g = setor9_g[0]
    setor9_valor_g = setor9_g[1]

    #Dados para Gráficos barChartCanvas
    ## Dicionário dct = dict((x, y) for x, y in barras1)
    ##print('ordenação 1 -------------',dct)
    ##aList = list(barras1)
    ##print('Lista -------------',aList)
    ##elemento = aList[0]

#--------------------------------------------------------------------------------------------------------



    # #nome SPD
    # for nome2 in maior:
    #     labels.append(nome2.factory)
    #     data.append(nome2.id)
    #     #print(nome2.factory)
    #     #print(nome2.id)


    # #nome marflex
    # for nome1 in menor:
    #     labels.append(nome1.factory)
    #     data.append(nome1.id)

    mes_str = datetime.today().strftime('%B')
    print(mes_str)

    context = {
        'os_list': os_list,
        'usuario':usuario,
        'data':mes_str,
        # RANKING DE FÁBRICAS QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES

        'fabrica0_nome':fabrica0_nome,
        'fabrica0_valor':fabrica0_valor,
        'fabrica1_nome':fabrica1_nome,
        'fabrica1_valor':fabrica1_valor,

        # RANKING DE FÁBRICAS QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES (Mês atual)

        'fabrica0_nome_g':fabrica0_nome_g,
        'fabrica0_valor_g':fabrica0_valor_g,
        'fabrica1_nome_g':fabrica1_nome_g,
        'fabrica1_valor_g':fabrica1_valor_g,

        # RANKING DE SETORES QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES
        'setor0_nome':setor0_nome,
        'setor0_valor':setor0_valor,
        'setor1_nome':setor1_nome,
        'setor1_valor':setor1_valor,
        'setor2_nome':setor2_nome,
        'setor2_valor':setor2_valor,
        'setor3_nome':setor3_nome,
        'setor3_valor':setor3_valor,
        'setor4_nome':setor4_nome,
        'setor4_valor':setor4_valor,
        'setor5_nome':setor5_nome,
        'setor5_valor':setor5_valor,
        'setor6_nome':setor6_nome,
        'setor6_valor':setor6_valor,
        'setor7_nome':setor7_nome,
        'setor7_valor':setor7_valor,
        'setor8_nome':setor8_nome,
        'setor8_valor':setor8_valor,        
        'setor9_nome':setor9_nome,
        'setor9_valor':setor9_valor,

        # RANKING DE SETORES QUE UTILIZAM OS SERVIÇOS E RESPECTIVAS QUANTIDADES (Mês atual)
        'setor0_nome_g':setor0_nome_g,
        'setor0_valor_g':setor0_valor_g,
        'setor1_nome_g':setor1_nome_g,
        'setor1_valor_g':setor1_valor_g,
        'setor2_nome_g':setor2_nome_g,
        'setor2_valor_g':setor2_valor_g,
        'setor3_nome_g':setor3_nome_g,
        'setor3_valor_g':setor3_valor_g,
        'setor4_nome_g':setor4_nome_g,
        'setor4_valor_g':setor4_valor_g,
        'setor5_nome_g':setor5_nome_g,
        'setor5_valor_g':setor5_valor_g,
        'setor6_nome_g':setor6_nome_g,
        'setor6_valor_g':setor6_valor_g,
        'setor7_nome_g':setor7_nome_g,
        'setor7_valor_g':setor7_valor_g,
        'setor8_nome_g':setor8_nome_g,
        'setor8_valor_g':setor8_valor_g,        
        'setor9_nome_g':setor9_nome_g,
        'setor9_valor_g':setor9_valor_g,

    }


    return render(request, 'dashboard.html', context)




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


