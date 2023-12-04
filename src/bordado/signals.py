from pprint import pprint

from django.db.models import Q
from django.db.models.signals import post_delete

from bordado.models import Lancamento


def acerta_saldos_cliente(cliente, data, id):
    print('acerta_saldos_cliente')
    lancamento = Lancamento.objects.filter(
        Q(cliente=cliente) & (
            Q(data__lte=data) | ( Q(data=data) & Q(id__lt=id) )
        )
    ).order_by('-data', '-id').first()
    if lancamento:
        saldo = lancamento.saldo_cliente
    else:
        saldo = 0
    print('acerta_saldos_cliente saldo', saldo)

    lancamentos = Lancamento.objects.filter(
        Q(cliente=cliente) & (
            Q(data__gt=data) | ( Q(data=data) & Q(id__gt=id) )
        )
    ).order_by('data', 'id')
    for lancamento in lancamentos:
        print('acerta_saldos_cliente', lancamento)
        print('novo saldo', saldo)
        saldo += lancamento.valor
        if lancamento.saldo_cliente != saldo:
            lancamento.saldo_cliente = saldo
            lancamento.calculando = True
            lancamento.save()


def acerta_saldos_empresa(data, id):
    print('acerta_saldos_empresa')
    lancamento = Lancamento.objects.filter(
        Q(data__lte=data) | ( Q(data=data) & Q(id__lt=id) )
    ).order_by('-data', '-id').first()
    if lancamento:
        saldo = lancamento.saldo_empresa
    else:
        saldo = 0
    print('acerta_saldos_empresa saldo', saldo)

    lancamentos = Lancamento.objects.filter(
        Q(data__gt=data) | ( Q(data=data) & Q(id__gt=id) )
    ).order_by('data', 'id')
    for lancamento in lancamentos:
        print('acerta_saldos_empresa', lancamento)
        print('novo saldo', saldo)
        saldo += lancamento.valor
        if lancamento.saldo_empresa != saldo:
            lancamento.saldo_empresa = saldo
            lancamento.calculando = True
            lancamento.save()


def post_delete_lancamento(sender, instance, *args, **kwargs):
    pprint('apagada', instance)
    cliente=instance.cliente
    data=instance.data
    id=instance.id
    acerta_saldos_cliente(cliente, data, id)
    acerta_saldos_empresa(data, id)


post_delete.connect(post_delete_lancamento, sender=Lancamento)