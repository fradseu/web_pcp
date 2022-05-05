
from queue import Empty
from django.shortcuts import redirect, render
from .models import Solicitacao
from .forms import Ferramentaria_form,Ferramentaria_form_report



# Create your views here.

def home(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'index.html',context)

    #return render(request, 'home.html')
    


def manut_list(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'manut_list.html',context)


def dashboard(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'dashboard.html',context)

    #return render(request, 'home.html')



def ferr_form(request,slug=0):

    if request.method == "GET":
        if slug==0:
            form = Ferramentaria_form()
            return render(request, 'manut_form.html',{'form':form})    
        else:
            editar = Solicitacao.objects.get(slug=slug)
            form = Ferramentaria_form(instance=editar)
            return render(request, 'manut_form.html',{'form':form})
    else:
        if slug==0:
            form = Ferramentaria_form(request.POST)
        else:
            editar = Solicitacao.objects.get(slug=slug)
            form = Ferramentaria_form(request.POST,instance=editar)
        if form.is_valid():
            form.save()
        return redirect('/manut_list/')

def manut_list(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'manut_list.html',context)


def manut_detail(request, slug):
    os_list = Solicitacao.objects.get(slug=slug)
    print(os_list.slug)
    
    if request.method == "POST":
        form1 = Ferramentaria_form_report(request.POST)
        

        if form1.is_valid():
            comments = form1.save(commit=False)
            comments.os_number = os_list
            comments.save()

            return redirect('manut_detail', slug= os_list.slug)
    else:
        form1 = Ferramentaria_form_report()

    return render(request, 'manut_detail.html', {'os_list':os_list, 'form1':form1})


