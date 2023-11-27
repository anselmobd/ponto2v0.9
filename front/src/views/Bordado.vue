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

function pedidoItemInseridoEmData(pedido_item) {
  var date = new Date(pedido_item.inserido_em)
  return date.toLocaleDateString('pt-br') + ' ' + date.toLocaleTimeString('pt-br');
}

onMounted(() => {
  getPedidoItens();
})
</script>

<template>
  <div>
    <h4 class="text-xl text-center bg-slate-800 text-slate-100">Pedido</h4>
    <table class="w-full">
      <thead>
        <tr>
          <th>Data</th>
          <th>Cliente</th>
          <th>Bordado</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!pedido_itens">
          <td colspan="4">Carregando últimos pedidos...</td>
        </tr>
        <tr
          v-for="pedido_item in pedido_itens"
          :key="pedido_item.id"
        >
          <td>{{pedidoItemInseridoEmData(pedido_item)}}</td>
          <td>{{pedido_item.pedido.cliente.apelido}}</td>
          <td>{{pedido_item.bordado.nome}}</td>
          <td>
            <button :disabled="editing" class="btn">Editar</button>
            <button :disabled="editing" class="btn">Apagar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
th, td {
  @apply border border-solid border-slate-300 text-center
}
</style>