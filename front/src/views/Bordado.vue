<script setup>
import { ref, onMounted } from 'vue'
import { axiosPrivate } from '../common/axiosPrivate.js';

const pedido_itens = ref(null)

function getPedidoItens() {
  const params = new URLSearchParams();
  params.append('format', 'json');

  axiosPrivate.get(
    '/bordado/api/pedido_item/',
    {params: params}
  )
  .then(response => {
    pedido_itens.value = response.data.results;
  })
  .catch(error => {
    console.log('error /bordado/api/pedido_item/', error)
  });
}

onMounted(() => {
  getPedidoItens();
})
</script>

<template>
  <div>
    <p>pedido_itens</p>
    {{pedido_itens}}
  </div>
</template>
