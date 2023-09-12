import axios from 'axios'

export default {
  template:
    /*html*/
    `
    <h4>Clientes</h4>
    <ul>
      <li v-for="cliente in clientes" :key="cliente.id">
        {{cliente.apelido}}
      </li>
    </ul>
    <h4>Pedido</h4>
    <ul>
      <li v-for="pedido_item in pedido_itens" :key="pedido_item.id">
        {{pedidoItemInseridoEmData(pedido_item)}} -
        {{pedido_item.pedido.cliente.apelido}} -
        {{pedido_item.bordado.nome}}
      </li>
    </ul>
    `,
  data() {
    return {
      clientes: {},
      pedido_itens: {}
    }
  },
  mounted() {
    axios.get('/bordado/api/clientes/?format=json')
    .then(response => {
      this.clientes = response.data.results;
    })
    .catch(error => {
      console.error('Erro ao obter clientes via API:', error);
    });
    axios.get('/bordado/api/pedido_item/?format=json')
    .then(response => {
      this.pedido_itens = response.data.results;
      console.log(this.pedido_itens);
    })
    .catch(error => {
      console.error('Erro ao obter pedido_itens via API:', error);
    });
  },
  methods: {
    pedidoItemInseridoEmData(pedido_item) {
      var date = new Date(pedido_item.inserido_em)
      return date.toLocaleDateString('pt-br');
    }
  }
}
