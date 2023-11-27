<script setup>
import { ref, onMounted } from 'vue'
import { axiosPrivate } from '../common/axiosPrivate.js';

const pedido_itens = ref(null);
const editing = ref(false);
const cliente = ref({
  input: '',
  error: '',
  list: []
});
const bordado = ref({
  input: '',
  error: '',
  list: []
});

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
    console.log('Erro ao obter pedido_itens via API:', error)
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
        <tr class="table__tr-input">
          <th>-</th>
          <th>
            <span class="text-sm text-red-700 font-bold" v-if="cliente.error" >{{ cliente.error }}<br /></span>
            <input
              class="mx-0.5 border border-solid border-slate-500"
              v-model.trim="cliente.input"
              :disabled="!editing"
              type="text"
              ref="inputCliente"
              placeholder="Cliente"
            >
          </th>
          <th>
            <span class="text-sm text-red-700 font-bold" v-if="bordado.error" >{{ bordado.error }}<br /></span>
            <input
              class="mx-0.5 border border-solid border-slate-500"
              v-model.trim="bordado.input"
              :disabled="!editing"
              type="text"
              ref="inputBordado"
              placeholder="Bordado"
            >
          </th>
          <th>
            -
          </th>
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
            <button :disabled="editing">Editar</button>
            <button :disabled="editing">Apagar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table__tr-input th {
  @apply font-normal 
}
th, td {
  @apply border border-solid border-slate-300 text-center
}
button {
  @apply mx-0.5 px-2 border border-solid border-slate-800 rounded-lg bg-cyan-600 font-bold text-slate-100
}
button:disabled {
  @apply bg-slate-500
}
</style>