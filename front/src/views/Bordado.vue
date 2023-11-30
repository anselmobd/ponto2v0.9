<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { storeToRefs } from 'pinia';
import { dateTime2Text } from "../utils/date.js";
import { useAuthStore } from '../stores/auth.js';
import { getPedidoItens, addClienteBordado, delClienteBordado } from '../api/pedidoItem.js';
import { getClientes } from '../api/cliente.js';
import { getBordados } from '../api/bordado.js';

const auth = useAuthStore();
// const { user } = storeToRefs(auth)

const pedido_itens = ref(null);
var pedido_itens_index = '';
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

// get set refs

function clearInputs() {
  cliente.value.input = '';
  bordado.value.input = '';
  pedido_itens_index = '';
}

function clearErrors() {
  cliente.value.error = '';
  bordado.value.error = '';
}

// DB API calls (do) and callbacks (cb)

function cbGetPedidoItens(data, error) {
  if (data) pedido_itens.value = data;
}

function cbGetClientes(data, error) {
  if (data) cliente.value.list = data;
}

function cbGetBordado(data, error) {
  if (data) bordado.value.list = data;
}

function doGetBordados() {
  bordado.value.list = [];
  if (cliente?.value?.input) {
    getBordados(cliente.value.input, cbGetBordado)
  }
}

function cbAddClienteBordado(data, error) {
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
  getClientes(cbGetClientes);
}

function doAddClienteBordado() {
  if (cliente?.value?.input && bordado?.value?.input) {
    addClienteBordado(
      cliente.value.input,
      bordado.value.input,
      cbAddClienteBordado
    );
  }
}

function cbDelClienteBordado(index) {
  if (index != -1) {
    apagaItemNaTela(index);
    getPedidoItens(cbGetPedidoItens);
  }
}

function doDelClienteBordado(index) {
  delClienteBordado(
    index,
    pedido_itens.value[index].id,
    cbDelClienteBordado
  );
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
  clearErrors();
  status.value = 'b';
}

function handleSalvaClick(event) {
  event.preventDefault();
  clearErrors();
  if (pedido_itens_index) {
    console.log('salva edit')
    pedidoItemParaTela('');
    clearInputs();
  } else {
    doAddClienteBordado();
  }
}

function handleEditarClick(event) {
  event.preventDefault();
  const index = event.target.value;
  cliente.value.input = pedido_itens.value[index].pedido.cliente.apelido;
  bordado.value.input = pedido_itens.value[index].bordado.nome;
  pedido_itens_index = index;
  status.value = 'e';
}

function handleApagarClick(event) {
  event.preventDefault();
  const index = event.target.value;
  const answer = window.confirm('Confirma apagar?')
  if (answer) doDelClienteBordado(index);
}

function reloadPage(event) {
  console.log('reload');
  location.reload();
}

// generic functions

function pedidoItemParaTela(pedido_item) {
  if (pedido_itens_index) {
    const index = pedido_itens_index;
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
  getPedidoItens(cbGetPedidoItens);
})

// watch
watch(status, async (newStatus) => {
  if (newStatus != 'b') {
    getClientes(cbGetClientes);
    inputClienteFocus();
  }
})

</script>

<template>
  <div>
    <h4 class="text-xl text-center font-bold bg-sky-900 text-slate-100">Pedido <a href="#" @click="reloadPage">&olarr;</a></h4>
    <table class="w-full">
      <thead>
        <tr>
          <th>Data</th>
          <th>Pedido</th>
          <th>Cliente</th>
          <th>Bordado</th>
          <th>Ações</th>
        </tr>
        <tr class="table__tr-input">
          <th>-</th>
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
              @focus="doGetBordados"
              type="text"
              name="bordado"
              id="bordado"
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
            >Salva</button>
            <button @click="handleCancelaClick" :hidden="status == 'b'" type="button">Cancela</button>
            <button @click="handleNovoClick" :hidden="status != 'b'" type="button">Novo</button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!pedido_itens">
          <td colspan="5">Carregando últimos pedidos...</td>
        </tr>
        <tr
          v-for="(pedido_item, index) in pedido_itens"
          :key="pedido_item.id"
        >
          <td :title="`key:${pedido_item.id} index:${index}`">{{pedidoItemInseridoEmData(pedido_item)}}</td>
          <td>{{pedido_item.id}}</td>
          <td>{{pedido_item.pedido.cliente.apelido}}</td>
          <td>{{pedido_item.bordado.nome}}</td>
          <td>
            <!-- <button
              :value="index"
              @click="handleEditarClick"
              :disabled="status != 'b'"
            >Editar</button> -->
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