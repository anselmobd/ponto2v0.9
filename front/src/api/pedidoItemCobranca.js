import { axiosPrivate } from '../common/axiosPrivate.js';

export function getPedidoItensCobrancas({
  page=1,
  cliente_apelido=null,
  callBack=()=>{}
}) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  if (page && page >1) {
    params.append('page', page);
  }
  if (cliente_apelido) {
    params.append('pedido_item__pedido__cliente__apelido', cliente_apelido);
  }
  axiosPrivate.get(
    '/bordado/api/pedido_item_cobranca/',
    {params: params}
  )
  .then(response => {
    callBack(response.data);
  })
  .catch(error => {
    console.error('Erro ao obter pedido_item_cobranca via API:', error)
    callBack(null, error);
  });
}

export function getPedidoItemCobranca({
  id=null,
  callBack=()=>{}
}) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  axiosPrivate.get(
    `/bordado/api/pedido_item_cobranca/${id}/`,
    {params: params}
  )
  .then(response => {
    callBack(response.data);
  })
  .catch(error => {
    console.error('Erro ao obter pedido_item_cobranca '+id+' via API:', error)
    callBack(null, error);
  });
}
