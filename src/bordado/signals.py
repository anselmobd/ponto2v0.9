from pprint import pprint

from django.db.models import Q
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver

from bordado.models import Lancamento


def acerta_saldos_cliente(cliente, data, id):
    print('acerta_saldos_cliente')
    lancamento = Lancamento.objects.filter(
        Q(cliente=cliente) & (
            Q(data__lt=data) | ( Q(data=data) & Q(id__lt=id) )
        )
    ).order_by('-data', '-id').first()
    print('anterior', lancamento)
    if lancamento:
        saldo = lancamento.saldo_cliente
    else:
        saldo = 0
    print('acerta_saldos_cliente saldo', saldo)

    lancamentos = Lancamento.objects.filter(
        Q(cliente=cliente) & (
            Q(data__gt=data) | ( Q(data=data) & Q(id__gte=id) )
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
        Q(data__lt=data) | ( Q(data=data) & Q(id__lt=id) )
    ).order_by('-data', '-id').first()
    print('anterior', lancamento)
    if lancamento:
        saldo = lancamento.saldo_empresa
    else:
        saldo = 0
    print('acerta_saldos_empresa saldo', saldo)

    lancamentos = Lancamento.objects.filter(
        Q(data__gt=data) | ( Q(data=data) & Q(id__gte=id) )
    ).order_by('data', 'id')
    for lancamento in lancamentos:
        print('acerta_saldos_empresa', lancamento)
        print('novo saldo', saldo)
        saldo += lancamento.valor
        if lancamento.saldo_empresa != saldo:
            lancamento.saldo_empresa = saldo
            lancamento.calculando = True
            lancamento.save()


@receiver(post_delete, sender=Lancamento)
def post_delete_lancamento(sender, instance, *args, **kwargs):
    print('post_delete_lancamento')
    pprint(instance)
    cliente=instance.cliente
    data=instance.data
    id=instance.id
    acerta_saldos_cliente(cliente, data, id)
    acerta_saldos_empresa(data, id)


@receiver(pre_save, sender=Lancamento)
def pre_save_lancamento(sender, instance, *args, **kwargs):
    instance.propagar = not instance.calculando
    instance.calculando = False


@receiver(post_save, sender=Lancamento)
def post_save_lancamento(sender, instance, *args, **kwargs):
    if instance.propagar:
        print('post_save_lancamento')
        pprint(instance)
        cliente=instance.cliente
        data=instance.data
        id=instance.id
        acerta_saldos_cliente(cliente, data, id)
        acerta_saldos_empresa(data, id)
