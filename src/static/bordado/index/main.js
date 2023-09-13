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
    <table>
      <thead>
        <tr>
            <th>Data</th>
            <th>Cliente</th>
            <th>Bordado</th>
            <th>Ações</th>
        </tr>
        <pedido-item-input
          @pedido-item-editing="pedidoItemEditing"
          :editing="editing"
        />
      </thead>
      <tbody>
        <pedido-item-list
          v-for="pedido_item in pedido_itens"
          :key="pedido_item.id"
          :pedido_item="pedido_item"
          :editing="editing"
        />
      </tbody>
    </table>
    `,
  data() {
    return {
      pedido_itens: {},
      editing: false
    }
  },
  mounted() {
    this.GetPedidoItens();
  },
  methods: {
    GetPedidoItens() {
      axios.get('/bordado/api/pedido_item/?format=json')
      .then(response => {
        this.pedido_itens = response.data.results;
      })
      .catch(error => {
        console.error('Erro ao obter pedido_itens via API:', error);
      });
    },
    pedidoItemEditing(value) {
      this.editing = value;      
    }
  }
}
