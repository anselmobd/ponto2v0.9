import { axiosPrivate } from '../common/axiosPrivate.js';

export function getPedidoItens(callBack) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  axiosPrivate.get(
    '/bordado/api/pedido_item/',
    {params: params}
  )
  .then(response => {
    callBack(response.data.results);
  })
  .catch(error => {
    console.error('Erro ao obter pedido_itens via API:', error)
    callBack(null, error);
  });
}

export function addClienteBordado(
  cliente_apelido,
  bordado_nome,
  callBack
) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  params.append('page_size', '999999');

  axiosPrivate.post(
    '/bordado/api/pedido_item/',
    {
      cliente: {apelido: cliente_apelido},
      bordado: {nome: bordado_nome}
    },
    {params: params},
  )
  .then(response => {
    callBack(response.data);
  })
  .catch(error => {
    console.error('Erro ao gravar cliente / bordado via API:', error);
    callBack(null, error.response.data);
  });
}
