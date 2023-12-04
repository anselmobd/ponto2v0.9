from pprint import pprint


__all__ = [
    'parcela_i_de_n_de_valor',
]


def parcela_i_de_n_de_valor(n, m, valor, decimais=2):
    parcela = round(valor / m, decimais)
    if n == m:
        return valor - (parcela * (m - 1))
    else:
        return parcela
