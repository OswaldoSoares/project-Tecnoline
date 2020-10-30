from django.db import models

# class Cliente(models.Model):
#     idCliente = models.AutoField(primary_key=True)
#     Apelido = models.CharField(max_length=20)
#     Nome = models.CharField(max_length=50)
#     Endereco = models.CharField(max_length=35, blank=True)
#     Bairro = models.CharField(max_length=20, blank=True)
#     CEP = models.CharField(max_length=9, blank=True)
#     Cidade = models.CharField(max_length=25, blank=True, default='SÃO PAULO')
#     Estado = models.CharField(max_length=2, blank=True, default='SP')
#     CNPJ = models.CharField(max_length=18, blank=True)
#     IE = models.CharField(max_length=15, blank=True)
#     Site = models.CharField(max_length=40, blank=True)
#
#     class Meta:
#         db_table = 'Cliente'
#         ordering = ['Apelido']
#
#     def __str__(self):
#         return self.Nome
#
#     objects = models.Manager()
