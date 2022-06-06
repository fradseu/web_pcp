from django import forms
from .models import Procedimento, Solicitacao,Ferr_report
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput

### Ferramentaria
#formulário de criação da Ordem de serviçõ Ferramentaria
class Ferramentaria_form(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ('fullname','type_service','factory','status_os','machine_code','sector','priority_type','issue_desctiption','propose_service')
        labels ={
            'fullname':'Quem solicitou',
            'type_service':'Tipo de Manutenção',
            'factory':'Fábrica',
            'status_os':'Status da OS:',
            'machine_code':'Cód. Máqina ou Ferramenta',
            'sector':'Setor',
            'priority_type':'Prioridade',
            'propose_service':'Propósito',
            'issue_desctiption':'Descrição do problema ou serviço'
        }
    def __init__(self, *args, **kwargs):
        super(Ferramentaria_form,self).__init__(*args, **kwargs)
        self.fields['type_service'].empty_label = "Selecione"
        self.fields['propose_service'].empty_label = "Selecione"
        self.fields['factory'].empty_label = "Selecione"
        self.fields['status_os'].empty_label = "Selecione"
        self.fields['sector'].empty_label = "Selecione"
        self.fields['priority_type'].empty_label = "Selecione"
        
### Ferramentaria
#formulário de report de serviçõ exdecutado na OS da Ferramentaria

class Ferramentaria_form_report(forms.ModelForm):


    class Meta:
        model = Ferr_report
        fields = ('name','data_1','hora_1','hora_2','body','procedimento','material','qtd_mat')
        widgets = {
            'data_1' : DatePickerInput(),
            'hora_1' : TimePickerInput(),
            'hora_2' : TimePickerInput(),
        }
        #name = forms.CharField(required=True)
        #data_1 = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'})) 
        #hora_1 = forms.TimeField(required=True,widget=forms.TimeInput(attrs={'type': 'time'})) 
        #hora_2 = forms.TimeField(required=True,widget=forms.TimeInput(attrs={'type': 'time'}))
        #body = forms.CharField(required=True)
        #data_1 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))                                                 
        
        labels ={
            'name':'Quem executou: ',
            'data_1':'Data: ',
            'hora_1':'Hora início: ',
            'hora_2':'Hora término: ',
            'body':'Descrição da tarefa: ',
            'procedimento':'Descrição da tarefa: ',
            'material': 'Material utilizado: ',
            'qtd_mat': 'Quantidade de material utilizado',
        }

class Status_form(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ('status_os',)
        labels ={
            'status_os':'Status da OS:',
        }
    def __init__(self, *args, **kwargs):
        super(Ferramentaria_form,self).__init__(*args, **kwargs)
        self.fields['status_os'].empty_label = "Selecione"