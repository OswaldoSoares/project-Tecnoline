from django.urls import path
from .views import index_servico, imprime_servico

urlpatterns = [
    path('', index_servico, name='index_servico'),
    path('imprime_servico/<int:idservico>/', imprime_servico, name='imprime_servico'),
]