from datetime import date
from django.shortcuts import redirect, render
from .models import Solicitacao,Ferr_report,Msg_day
from .forms import Ferramentaria_form,Ferramentaria_form_report
import io
from django.http import FileResponse
import reportlab
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import messages
import os
from datetime import datetime


###############################################

#página Inicial.
def home(request):
    #mensagem do dia, um pequeno motivacional para descontrair.
    msg_date = datetime.today().strftime('%Y-%m-%d')

    try:
        editar = Msg_day.objects.get(current_day=msg_date)
    except:    
        editar = datetime.today().strftime('%Y-%m-%d')
        print('---------------')
        print(editar)


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
def manut_list(request):
    
    os_list = Solicitacao.objects.all()    
    # configuração paginação
    p = Paginator(Solicitacao.objects.all(), 50)
    page = request.GET.get('page')
    ordens = p.get_page(page)
    nums = "a" * ordens.paginator.num_pages
    context = {
        'os_list': os_list,
        'ordens': ordens,
        'nums': nums
        }
    return render(request, 'manut_list.html',context)


#Página do dashboard.
def dashboard(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'dashboard.html',context)





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
                print('tentativa')
                print(form.status_os)
            if form.is_valid():
                manut_print = form.save()                
                print('------------------------------')
                print('Os Criada')
                print('Número da OS: ',manut_print.id)                
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
                                          
                return render(request, 'manut_print.html',contexto)


#Em um futuro distante, tentarei renderizar a página através de Query
def manut_impressao(request):    
    
    return render(request, 'manut_print.html')



#Página de detalhe da Os
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
            return redirect('manut_detail', slug= os_list.slug)
    else:
        form1 = Ferramentaria_form_report()
    return render(request, 'manut_detail.html', {'os_list':os_list, 'form1':form1})


#Apagar a Ordem de Serviço
def form_delete(request, id):
    os_list = Solicitacao.objects.get(pk=id)
    print('------------------------------')
    print('Atividade de OS deletada')
    print('OS: ',os_list)
    os_list.delete()
    return redirect('/manut_list/')


#Apagar atividades das OS (registros)
def apagar_delete(request, id):
    os_number = Ferr_report.objects.get(pk=id)
    print('------------------------------')
    print(request.META.get('HTTP_REFERER'))
    print('OS:',os_number.id)
    print('Atividade de os deletada')
    os_number.delete()

    messages.add_message(request, messages.INFO, 'Atividade de os deletada.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
    #return redirect('/manut_list/')



class msg_do_dia:
    def msg_dia():
        pass


