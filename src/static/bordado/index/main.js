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
          @pedido-item-inserting="pedidoItemInserting"
          @pedido-item-para-tela="pedidoItemParaTela"
          :editing="editing"
        />
      </thead>
      <tbody>
        <tr v-if="pedido_itens == null">
          <td colspan="4">Carregando dados...</td>
        </tr>
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
      pedido_itens: null,
      editing: false,
      inserting: false
    }
  },
  watch: {
    inserting: function (value) {
      if (value) {
        this.editing = true;
      };
    },
    editing: function (value) {
      if (!value) {
        this.inserting = false;
      };
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
    },
    pedidoItemInserting() {
      this.inserting = true;
    },
    pedidoItemParaTela(pedido_item) {
      if (this.inserting) {
        this.pedido_itens.unshift(pedido_item);
        this.editing = false;
      }
    }
  }
}
