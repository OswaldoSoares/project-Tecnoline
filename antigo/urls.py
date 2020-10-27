from django.urls import path
from .views import index_servico

urlpatterns = [
    path(
        '',
        index_servico,
        name='index_servico'
    ),
]