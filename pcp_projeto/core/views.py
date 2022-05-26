

from django.shortcuts import redirect, render
from .models import Solicitacao,Ferr_report
from .forms import Ferramentaria_form,Ferramentaria_form_report
import io
from django.http import FileResponse
import reportlab
from reportlab.pdfgen import canvas



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

def some_view():
            # Create a file-like buffer to receive PDF data.
            buffer = io.BytesIO()

            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(100, 100, "Hello world.")

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()

            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

class ferram_class:
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
                manut_print = form.save()
                
                print('------------------------------')
                print('Número da id: ',manut_print.id)
                
                impress_id = manut_print.id

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


def manut_impressao(request):
    
    return render(request, 'manut_print.html')

                


def manut_list(request):
    os_list = Solicitacao.objects.all()
    context = {
        'os_list': os_list
    }
    return render(request, 'manut_list.html',context)


def manut_detail(request, slug):
    os_list = Solicitacao.objects.get(slug=slug)
        
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


def form_delete(request, id):
    os_list = Solicitacao.objects.get(pk=id)
    os_list.delete()

    return redirect('/manut_list/')


def apagar_delete(request, id):
    os_number = Ferr_report.objects.get(pk=id)
    os_number.delete
    return redirect('/manut_list/')



class msg_do_dia:
    def msg_dia():
        pass


