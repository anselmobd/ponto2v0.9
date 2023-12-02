<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, watch } from 'vue'
import { getPedidoItem, saveFechamento, delFechamento } from '../api/pedidoItem.js';
import { dateTime2Text, date2InputText } from "../utils/date.js";
import { ptBrCurrencyFormat } from "../utils/numStr.js";
import { floatRound } from "../utils/number.js";

// TODO
// - valores: não permitir valores com fração de centavo

const route = useRoute();

// valores recebidos de DB

const pedido_item = ref('')
const inserido_em = ref(null)

// variaveis comuns

  // para data de entrega
const dataAtual = new Date();
const doisDiasDepois = new Date(dataAtual.getTime() + (2 * 86400000));
const strDoisDiasDepois = date2InputText(doisDiasDepois);

  // auxiliar para cálculos
var inputValorFinalFocused = false;

// valores em inputs

const data_entrega = ref(strDoisDiasDepois)
const quantidade = ref(0)
const valor_unitario = ref(0)
const programacao = ref(0)
const ajuste = ref(0)

// outros valores reativos

const valor = ref(0)
const valor_final = ref(0)
const alerta = ref('')

// DB API calls (do) and callbacks (cb)

function cbPedidoItem(data, error) {
  if (data) {
    pedido_item.value = data;
    const date = new Date(pedido_item.value.inserido_em);
    inserido_em.value = dateTime2Text(date);
    quantidade.value = pedido_item.value.quantidade;
    valor_unitario.value = parseFloat(pedido_item.value.preco);
    programacao.value = parseFloat(pedido_item.value.programacao);
    ajuste.value = parseFloat(pedido_item.value.ajuste);
    if (pedido_item.value.pedido.entrega) {
      data_entrega.value = pedido_item.value.pedido.entrega;
    } else {
      data_entrega.value = strDoisDiasDepois;
    }
  }
}

function doGetPedidoItem() {
  getPedidoItem({
    id: route.params.id,
    callBack: cbPedidoItem
  });
}

function cbSaveFechamento(data, error) {
  if (data) {
    console.log('salvo fechamento')
    console.log(data);
  }
  if (error) {
    console.log('erro salvando fechamento')
    console.log(error);
  };
}

function doSaveFechamento() {
  console.log('doSaveFechamento');
  if (
    data_entrega?.value &&
    quantidade?.value &&
    valor_unitario?.value
  ) {
    console.log('doSaveFechamento if');
    saveFechamento({
      id: route.params.id,
      data_entrega: data_entrega.value,
      quantidade: quantidade.value,
      valor_unitario: valor_unitario.value,
      programacao: programacao.value,
      ajuste: ajuste.value,
      callBack: cbSaveFechamento,
    });
  }
}

function cbDelFechamento(data, error) {
  if (data) {
    console.log('apagado fechamento')
    console.log(data);
    doGetPedidoItem();
    calcValor();
    calcValorFinal();
  }
  if (error) {
    console.log('erro apagando fechamento')
    console.log(error);
  };
}

function doDelFechamento() {
  console.log('doDelFechamento');
  delFechamento({
    id: route.params.id,
    callBack: cbDelFechamento,
  });
}

// events

function formGrava() {
  console.log('grava');
  doSaveFechamento();
}

function handleApagaClick(event) {
  event.preventDefault();
  doDelFechamento();
}

// Lifecycle Hooks

onMounted(() => {
  doGetPedidoItem();
  calcValor();
  calcValorFinal();
})

// watch

watch(quantidade, (_) => {
  calcValor();
  calcValorFinal();
})

watch(valor_unitario, (_) => {
  calcValor();
  calcValorFinal();
})

watch(programacao, (_) => {
  calcValorFinal();
})

watch(ajuste, (_) => {
  if (!inputValorFinalFocused) {
    calcValorFinal();
  }
})

watch(valor_final, (_) => {
  if (inputValorFinalFocused) {
    calcAjuste();
  }
})

// generic functions

function calcValor() {
  const calculo = quantidade.value * valor_unitario.value;
  valor.value = ptBrCurrencyFormat.format(calculo);
}

function calcValorFinal() {
  const calculo = quantidade.value * valor_unitario.value
    + programacao.value + ajuste.value;
  valor_final.value = floatRound(calculo, 2);
}

function calcAjuste() {
  const calculo = valor_final.value
    - quantidade.value * valor_unitario.value
    - programacao.value;
  ajuste.value = floatRound(calculo, 2);
}

</script>

<template>
  <div>
    <h2 class="my-4 font-bold text-xl">Fechando pedido <span class="text-indigo-700">{{ route.params.id }}</span></h2>
    <div v-if="pedido_item">
      <table class="w-full">
        <thead>
          <tr>
            <th>Usuário</th>
            <th>Data</th>
            <th>Cliente</th>
            <th>Bordado</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ pedido_item.usuario.username }}</td>
            <td>{{inserido_em}}</td>
            <td>{{pedido_item.pedido.cliente.apelido}}</td>
            <td>{{pedido_item.bordado.nome}}</td>
          </tr>
        </tbody>
      </table>
      <h3 class="my-4 font-bold text-lg">Dados do bordado</h3>
        <form @submit.prevent="formGrava()">
        <table class="w-full">
          <thead>
            <tr>
              <th><label for="data_entrega">Data de entrega</label></th>
              <th><label for="quantidade">Quantidade</label></th>
              <th><label for="valor_unitario">Valor unitário</label></th>
              <th>Valor</th>
              <th><label for="programacao">Programação</label></th>
              <th><label for="ajuste">Ajuste</label></th>
              <th>Valor final</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <input
                  class="px-2 py-1 w-40 border-2 rounded"
                  type="date"
                  name="data_entrega"
                  id="data_entrega"
                  v-focus
                  v-model="data_entrega"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  name="quantidade"
                  id="quantidade"
                  placeholder="0"
                  v-model="quantidade"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="valor_unitario"
                  id="valor_unitario"
                  placeholder="0,00"
                  v-model="valor_unitario"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                 {{ valor }}
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="programacao"
                  id="programacao"
                  placeholder="0,00"
                  v-model="programacao"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="ajuste"
                  id="ajuste"
                  placeholder="0,00"
                  v-model="ajuste"
                  @input="alerta = ''"
                  required>
              </td>
              <td>
                 <input
                  class="px-2 py-1 w-24 border-2 rounded"
                  type="number"
                  step="0.01"
                  name="valor_final"
                  id="valor_final"
                  placeholder="0,00"
                  v-model="valor_final"
                  @focus="inputValorFinalFocused = true"
                  @blur="inputValorFinalFocused = false"
                  @input="alerta = ''"
                  required>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="alerta" class="my-4 text-red-600">{{ alerta }}</p>
        <p class="flex flex-row-reverse place-content-between">
          <button
            class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100"
            type="submit"
          >Grava</button>
          <button
            class="px-2 py-1 rounded-xl bg-sky-700 font-bold text-slate-100"
            @click="handleApagaClick"
          >Apaga fechamento</button>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
table  {
  @apply my-4
}
th, td {
  @apply border border-solid border-slate-300 text-center
}
</style>
