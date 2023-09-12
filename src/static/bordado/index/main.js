import axios from 'axios'
import PedidoItemInput from 'bordado_index/PedidoItemInput.js'
import PedidoItemList from 'bordado_index/PedidoItemList.js'

export default {
  components: {
    PedidoItemInput,
    PedidoItemList,
  },
  template:
    /*html*/
    `
    <h4 class="tela">Pedido</h4>
    <!--form @submit.prevent="onSubmit"-->
      <table>
        <thead>
          <tr>
              <th>Data</th>
              <th>Cliente</th>
              <th>Bordado</th>
              <th>Ações</th>
          </tr>
          <pedido-item-input />
        </thead>
        <tbody>
          <pedido-item-list
            v-for="pedido_item in pedido_itens"
            :key="pedido_item.id"
            :pedido_item="pedido_item"
          />
        </tbody>
      </table>
    <!--/form-->
    <h4>Clientes</h4>
    <ul>
      <li v-for="cliente in clientes" :key="cliente.id">
        {{cliente.apelido}}
      </li>
    </ul>
    `,
  data() {
    return {
      clientes: {},
      pedido_itens: {},
    }
  },
  mounted() {
    this.GetPedidoItens();
    axios.get('/bordado/api/clientes/?format=json')
    .then(response => {
      this.clientes = response.data.results;
    })
    .catch(error => {
      console.error('Erro ao obter clientes via API:', error);
    });
  },
  methods: {
    GetPedidoItens() {
      axios.get('/bordado/api/pedido_item/?format=json')
      .then(response => {
        this.pedido_itens = response.data.results;
        console.log(this.pedido_itens);
      })
      .catch(error => {
        console.error('Erro ao obter pedido_itens via API:', error);
      });
    }
  }
}
