<script setup>
import router from '@/router'
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
const pedido_itens_next = ref(1);
const pedido_itens_loading = ref(false);
const pedido_itens_filtro_apelido = ref(null);
var pedido_itens_index = '';

const status = ref('b'); // browsing inserting filtering
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

// get set refs

function clearInputs(cliente_apelido = '') {
  cliente.value.input = cliente_apelido;
  bordado.value.input = '';
  pedido_itens_index = '';
}

function clearErrors() {
  cliente.value.error = '';
  bordado.value.error = '';
}

// DB API calls (do) and callbacks (cb)

function cbGetFirstsPedidoItens(data, error) {
  if (data) {
    if (data?.results) pedido_itens.value = data.results;
    pedido_itens_next.value = data.next;
  }
  pedido_itens_loading.value = false;
}

function doGetFirstsPedidoItens() {
  pedido_itens_next.value = 1;
  doGetPedidoItens(cbGetFirstsPedidoItens)
}

function cbGetMorePedidoItens(data, error) {
  if (data) {
    if (data?.results) pedido_itens.value = pedido_itens.value.concat(data.results);
    pedido_itens_next.value = data.next;
  }
  pedido_itens_loading.value = false;
}

function doGetMorePedidoItens() {
  doGetPedidoItens(cbGetMorePedidoItens)
}

function doGetPedidoItens(callBack) {
  pedido_itens_loading.value = true;
  getPedidoItens({
    page: pedido_itens_next.value,
    cliente_apelido: pedido_itens_filtro_apelido.value,
    callBack: callBack
  });
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
    doGetFirstsPedidoItens();
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
    doGetFirstsPedidoItens();
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
  clearInputs(pedido_itens_filtro_apelido.value);
  status.value = 'i';
}

function handleCancelaClick(event) {
  event.preventDefault();
  clearInputs();
  clearErrors();
  status.value = 'b';
}

function handleSalvaFiltraClick(event) {
  event.preventDefault();
  if (status.value == 'i') {
    clearErrors();
    status.value = 'b';
    doAddClienteBordado();
  } else if (status.value == 'f') {
    pedido_itens_filtro_apelido.value = cliente.value.input;
    clearInputs();
    status.value = 'b';
    doGetFirstsPedidoItens();
  }
}

function handleFiltroClick(event) {
  event.preventDefault();
  clearInputs();
  status.value = 'f';
}

function handleCancelaFiltroClick(event) {
  event.preventDefault();
  pedido_itens_filtro_apelido.value = null;
  doGetFirstsPedidoItens();
}

function handleApagarClick(event) {
  event.preventDefault();
  const index = event.target.value;
  const answer = window.confirm('Confirma apagar?')
  if (answer) doDelClienteBordado(index);
}

function reloadPedidoItens(event) {
  event.preventDefault();
  doGetFirstsPedidoItens();
}

function handleMaisPedidosClick(event) {
  event.preventDefault();
  doGetMorePedidoItens();
}

function handleFechandoClick(event) {
  event.preventDefault();
  const id = event.target.value;
  router.push({ name: 'fechando', params: { id: id } });
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

function inputBordadoFocus() {
  nextTick(() => {
    inputBordado.value.focus();
  })
}

// Lifecycle Hooks

onMounted(() => {
  doGetFirstsPedidoItens();
})

// watch
watch(status, (newStatus) => {
  if (newStatus != 'b') {
    getClientes(cbGetClientes);
    if (newStatus == 'f') {
      inputClienteFocus();
    } else if (newStatus == 'i') {
      if (pedido_itens_filtro_apelido.value) {
        inputBordadoFocus();
      } else {
        inputClienteFocus();
      }
    }
  }
})

</script>

<template>
  <div>
    <h4 class="text-xl text-center font-bold bg-sky-900 text-slate-100">Pedido <a @click="reloadPedidoItens">&olarr;</a></h4>
    <table class="w-full">
      <thead>
        <tr>
          <th>Usuário</th>
          <th>Data</th>
          <th>Pedido</th>
          <th>Cliente<span v-if="pedido_itens_filtro_apelido" ><br/><span class="text-indigo-700">{{ pedido_itens_filtro_apelido }}</span><a href="#" class="button" @click="handleCancelaFiltroClick">&cross;</a></span></th>
          <th>Bordado</th>
          <th>Ações</th>
        </tr>
        <tr class="table__tr-input">
          <th colspan="3">
            <span class="font-bold" v-if="status == 'i'">Inserindo</span>
            <span class="font-bold" v-if="status == 'f'">Filtrando</span>
          </th>
          <th>
            <span class="text-sm text-red-700 font-bold" v-if="cliente.error" >{{ cliente.error }}<br /></span>
            <input
              class="mx-0.5 border border-solid border-slate-500 disabled:border-slate-200 rounded"
              v-model.trim="cliente.input"
              :disabled="status == 'b' || (status == 'i' && pedido_itens_filtro_apelido)"
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
              class="mx-0.5 border border-solid border-slate-500 disabled:border-slate-200 rounded"
              v-model.trim="bordado.input"
              :disabled="status != 'i'"
              @focus="doGetBordados"
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
              @click="handleSalvaFiltraClick"
              :hidden="status == 'b'"
            ><span v-if="status == 'i'">Salva</span><span v-if="status == 'f'">Filtra</span></button>
            <button
              type="button"
              @click="handleCancelaClick"
              :hidden="status == 'b'"
            >Cancela</button>
            <button
              type="button"
              @click="handleNovoClick"
              :hidden="status != 'b'"
            >Novo</button>
            <button
              type="button"
              @click="handleFiltroClick"
              :hidden="status != 'b'"
            >Filtro</button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="pedido_itens_loading">
          <td colspan="6">
            <span v-if="pedido_itens_next == 1 && !pedido_itens">Carregando</span>
            <span v-if="pedido_itens_next == 1 && pedido_itens">Recarregando</span>
            <span v-if="pedido_itens_next == 1"> os pedidos mais recentes...</span>
            <span v-if="pedido_itens_next > 1">Carregando mais pedidos...</span>
          </td>
        </tr>
        <tr
          v-for="(pedido_item, index) in pedido_itens"
          :key="pedido_item.id"
        >
          <td>{{ pedido_item.usuario.username }}</td>
          <td>{{pedidoItemInseridoEmData(pedido_item)}}</td>
          <td>{{pedido_item.id}}</td>
          <td>{{pedido_item.pedido.cliente.apelido}}</td>
          <td>{{pedido_item.bordado.nome}}</td>
          <td>
            <button
              :value="index"
              @click="handleApagarClick"
              :disabled="status != 'b'"
            >Apagar</button>
            <button
              :value="pedido_item.id"
              @click="handleFechandoClick"
              :disabled="status != 'b'"
            >&vrtri;</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button
      v-if="pedido_itens_next"
      @click="handleMaisPedidosClick"
    >Mais pedidos</button>
  </div>
</template>

<style scoped>
.table__tr-input th {
  @apply font-normal 
}
th, td {
  @apply border border-solid border-slate-300 text-center
}
button, .button {
  @apply mx-0.5 my-[1px] px-2 py-0.5 rounded-lg bg-sky-700 font-bold text-slate-100
}
button:disabled {
  @apply bg-slate-500
}
</style>