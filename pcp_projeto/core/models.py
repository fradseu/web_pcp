from django.db import models
from django.utils.text import slugify
import random
import string

#from blog.utils import unique_slug_generator

# Create your models here.


class Factory(models.Model):
    title = models.CharField(max_length=20)
    #função para nomear os itens que vem da bd
    # self pois se não nomear fica como item 1, item 2, item 3 e por ai vai. 
    def __str__(self):
        return self.title

class Sector(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title


class Priority(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Statusos(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Type_service(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title
		
class Solicitacao(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=30)
    slug = models.SlugField('Slug', editable=False)
    factory = models.ForeignKey(Factory, on_delete= models.CASCADE)
    machine_code = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete= models.CASCADE)
    priority_type = models.ForeignKey(Priority, on_delete= models.CASCADE)
    date_create = models.DateField(auto_now_add=True)
    hour_arrive = models.TimeField(auto_now_add=True)
    issue_desctiption = models.CharField(max_length=150)
    status_os = models.ForeignKey(Statusos, on_delete= models.CASCADE)
    type_service = models.ForeignKey(Type_service,max_length=50, on_delete= models.CASCADE)
 
    
    class Meta:
        ordering = ['-date_create']

#    def cod():
 #       allowed_chars = ''.join((string.ascii_letters, string.digits))
  #      unique_id = ''.join(random.choice(allowed_chars) for _ in range(32))
   #     unique_id

    def save(self, *args, **kwargs):
        value = self.factory
        self.slug = slugify(value, allow_unicode=True)
        Solicitacao.objects.filter(slug=self.factory)
        allowed_chars = ''.join((string.digits))
        unique_id = ''.join(random.choice(allowed_chars) for _ in range(8))
        unique_id
        self.slug += unique_id
        super().save(*args, **kwargs)



class Ferr_report(models.Model):
    id = models.AutoField(primary_key=True)
    os_number = models.ForeignKey(Solicitacao, related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    data_1 = models.DateField()
    hora_1 = models.TimeField()
    hora_2 = models.TimeField()
    body = models.TextField(max_length=255)

    

    class Meta:
        ordering = ['data_1']
       

##### fim do novo modelo ####

### tudo que está abaixo era aprendizado

