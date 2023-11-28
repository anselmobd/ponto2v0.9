<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth.js';
import { axiosPrivate } from '../common/axiosPrivate.js';

const auth = useAuthStore();
// const { user } = storeToRefs(auth)

const pedido_itens = ref(null);
const status = ref('b'); // browsing editing inserting
const cliente = ref({
  input: '',
  error: '',
  list: [
    'casd',
    'casdfgggg',
    'czxcv'
  ]
});
const bordado = ref({
  input: '',
  error: '',
  list: [
    'basd',
    'basdfgggg',
    'bzxcv'
  ]
});

const inputCliente = ref(null)
const inputBordado = ref(null)

// get set refs

function clearInputs() {
  cliente.value.input = '';
  bordado.value.input = '';
}

// get set db

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

// event functions

function handleNovoClick(event) {
  event.preventDefault();
  clearInputs();
  status.value = 'i';
}

// generic functions

function pedidoItemInseridoEmData(pedido_item) {
  var date = new Date(pedido_item.inserido_em)
  return date.toLocaleDateString('pt-br') + ' ' + date.toLocaleTimeString('pt-br');
}

function inputClienteFocus() {
  nextTick(() => {
    inputCliente.value.focus();
  })
}

// Lifecycle Hooks

onMounted(() => {
  getPedidoItens();
})

// watch
watch(status, async (newStatus) => {
  if (newStatus != 'b') {
    inputClienteFocus();
  }
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
              :disabled="status == 'b'"
              type="text"
              name="cliente"
              id="cliente"
              ref="inputCliente"
              placeholder="Cliente"
              list="cliente-list"
            >
            <datalist id="cliente-list">
              <option v-for="cliente1 in cliente.list">{{cliente1}}</option>
            </datalist>
          </th>
          <th>
            <span class="text-sm text-red-700 font-bold" v-if="bordado.error" >{{ bordado.error }}<br /></span>
            <input
              class="mx-0.5 border border-solid border-slate-500"
              v-model.trim="bordado.input"
              :disabled="status == 'b'"
              type="text"
              name="bordado"
              id="bordado"
              ref="inputBordado"
              placeholder="Bordado"
              list="bordado-list"
            >
            <datalist id="bordado-list">
              <option v-for="bordado1 in bordado.list">{{bordado1}}</option>
            </datalist>
          </th>
          <th>
            <button @click="handleNovoClick" :hidden="status != 'b'" type="button">Novo</button>
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
            <button :disabled="status != 'b'">Editar</button>
            <button :disabled="status != 'b'">Apagar</button>
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