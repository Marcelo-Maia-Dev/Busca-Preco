from django.db import models

class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    preco = models.DecimalField(decimal_places=2,max_digits=12)
    site = models.TextField(max_length=255)
    data_cotacao = models.DateField()
    link_imagem = models.TextField(max_length=500,default='https://placehold.jp/3d4070/ffffff/150x150.png') 
    
