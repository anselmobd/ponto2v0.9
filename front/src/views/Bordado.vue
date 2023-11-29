<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { storeToRefs } from 'pinia';
import { dateTime2Text } from "../utils/date.js";
import { useAuthStore } from '../stores/auth.js';
import { axiosPrivate } from '../common/axiosPrivate.js';
import { getPedidoItensCB } from '../api/pedidoItem.js';
import { getClientesCB } from '../api/cliente.js';
import { getBordadosCB } from '../api/bordado.js';

const auth = useAuthStore();
// const { user } = storeToRefs(auth)

const pedido_itens = ref(null);
const status = ref('b'); // browsing editing inserting
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

// componentes do template que serão referenciados

const inputCliente = ref(null)
const inputBordado = ref(null)
const buttonSalva = ref(null)

// get set refs

function clearInputs() {
  cliente.value.input = '';
  bordado.value.input = '';
  buttonSalva.value.value = '';
}

// API DB "callbacks"

function pedidoItensCB(data, error) {
  if (data) pedido_itens.value = data;
}

function clientesCB(data, error) {
  if (data) cliente.value.list = data;
}

function bordadoCB(data, error) {
  if (data) bordado.value.list = data;
}

function getBordados() {
  bordado.value.list = [];
  if (cliente?.value?.input) {
    getBordadosCB(cliente.value.input, bordadoCB)
  }
}

function clienteBordadoCB(data, error) {
  if (data) {
    pedidoItemParaTela(data);
    clearInputs();
  }
  if (error) {
    if ('apelido' in error) {
      cliente.value.error = error.apelido.join('|');
    }
    if ('nome' in error) {
      bordado.value.error = error.nome.join('|');
    }
  };
  getClientesCB(clientesCB);
}

function setClienteBordadoCB(callBack) {
  const params = new URLSearchParams();
  params.append('format', 'json');
  params.append('page_size', '999999');

  axiosPrivate.post(
    '/bordado/api/pedido_item/',
    {
      cliente: {
        apelido: cliente.value.input
      },
      bordado: {
        nome: bordado.value.input
      },
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

// event functions

function handleNovoClick(event) {
  event.preventDefault();
  clearInputs();
  status.value = 'i';
}

function handleCancelaClick(event) {
  event.preventDefault();
  clearInputs();
  status.value = 'b';
}

function handleSalvaClick(event) {
  event.preventDefault();
  cliente.value.error = '';
  bordado.value.error = '';
  if (buttonSalva.value.value) {
    console.log('salva edit')
    pedidoItemParaTela('');
    clearInputs();
  } else {
    setClienteBordadoCB(clienteBordadoCB);
  }
}

function handleEditarClick(event) {
  event.preventDefault();
  const index = event.target.value;
  cliente.value.input = pedido_itens.value[index].pedido.cliente.apelido;
  bordado.value.input = pedido_itens.value[index].bordado.nome;
  buttonSalva.value.value = index;
  status.value = 'e';
}

function handleApagarClick(event) {
  event.preventDefault();
  const index = event.target.value;
  console.log('apaga', index)
  apagaItemNaTela(index);
}

// generic functions

function pedidoItemParaTela(pedido_item) {
  if (buttonSalva.value.value) {
    const index = buttonSalva.value.value;
    pedido_itens.value[index].pedido.cliente.apelido = cliente.value.input;
    pedido_itens.value[index].bordado.nome = bordado.value.input;
  } else {
    pedido_itens.value.unshift(pedido_item);
  }
  status.value = 'b';
}

function apagaItemNaTela(index) {
  pedido_itens.value.splice(index, 1);
}

function pedidoItemInseridoEmData(pedido_item) {
  const date = new Date(pedido_item.inserido_em)
  return dateTime2Text(date);
}

function inputClienteFocus() {
  nextTick(() => {
    inputCliente.value.focus();
  })
}

// Lifecycle Hooks

onMounted(() => {
  getPedidoItensCB(pedidoItensCB);
})

// watch
watch(status, async (newStatus) => {
  if (newStatus != 'b') {
    getClientesCB(clientesCB);
    inputClienteFocus();
  }
})

</script>

<template>
  <div>
    <h4 class="text-xl text-center font-bold bg-sky-900 text-slate-100">Pedido</h4>
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
              @focus="getBordados"
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
            <button
              type="button"
              @click="handleSalvaClick"
              :hidden="status == 'b'"
              value=""
              ref="buttonSalva"
            >Salva</button>
            <button @click="handleCancelaClick" :hidden="status == 'b'" type="button">Cancela</button>
            <button @click="handleNovoClick" :hidden="status != 'b'" type="button">Novo</button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!pedido_itens">
          <td colspan="4">Carregando últimos pedidos...</td>
        </tr>
        <tr
          v-for="(pedido_item, index) in pedido_itens"
          :key="pedido_item.id"
        >
          <td :title="`key:${pedido_item.id} index:${index}`">{{pedidoItemInseridoEmData(pedido_item)}}</td>
          <td>{{pedido_item.pedido.cliente.apelido}}</td>
          <td>{{pedido_item.bordado.nome}}</td>
          <td>
            <button
              :value="index"
              @click="handleEditarClick"
              :disabled="status != 'b'"
            >Editar</button>
            <button
              :value="index"
              @click="handleApagarClick"
              :disabled="status != 'b'"
            >Apagar</button>
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
  @apply mx-0.5 my-[1px] px-2 py-0.5 rounded-lg bg-sky-700 font-bold text-slate-100
}
button:disabled {
  @apply bg-slate-500
}
</style>