<script setup>
import { ref, onMounted } from 'vue'
import { axiosPrivate } from '../common/axiosPrivate.js';

const pedido_itens = ref(null)

function getPedidoItens(tentativa = 1) {
  console.log('getPedidoItens', tentativa);

  const params = new URLSearchParams();
  params.append('format', 'json');
  console.log(params);

  var result = 0;

  axiosPrivate.get(
    '/bordado/api/pedido_item/',
    {params: params}
  )
  .then(response => {
    console.log('getPedidoItens then');
    console.log(response);
    console.log(response.data.results);
    pedido_itens.value = response.data.results;
    result = response.status;
  })
  .catch(error => {
    console.log('getPedidoItens catch');
    console.log('Erro ao obter pedido_itens via API:', error);
    console.log(error.response.status);
    result = error.response.status;
  })
  .finally(function () {
    console.log('getPedidoItens finally');
  });
  console.log('getPedidoItens fim');
}

onMounted(() => {
  console.log('onMounted');
  getPedidoItens();
  console.log(pedido_itens);
})
</script>

<template>
  <div>
    <p>pedido_itens</p>
    {{pedido_itens}}
  </div>
</template>
