import axios from 'axios'
import PedidoItemList from 'bordado_index/PedidoItemList.js'

export default {
  components: {
    PedidoItemList,
  },
  template:
    /*html*/
    `
    <h4 class="tela">Pedido</h4>
    <form @submit.prevent="onSubmit">
      <table>
        <thead>
          <tr>
              <th>Data</th>
              <th>Cliente</th>
              <th>Bordado</th>
              <th>Ações</th>
          </tr>
          <tr class="input-row">
              <td>-</td>
              <td><input type="text" id="cliente" placeholder="Cliente"></td>
              <td><input type="text" id="bordado" placeholder="Bordado"></td>
              <td>
                  <button class="btn">Salvar</button>
                  <button class="btn" id="adicionar">Novo</button>
              </td>
          </tr>
        </thead>
        <tbody>
          <pedido-item-list
            v-for="pedido_item in pedido_itens"
            :key="pedido_item.id"
            :pedido_item="pedido_item"
          />
        </tbody>
      </table>
    </form>
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
      cliente: '',
      bordado: '',
      error: {
        cliente: '',
        bordado: ''
      }
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
    },
    onSubmit() {
      let newPedido = {
        cliente: this.cliente,
        bordado: this.bordado
      }
      console.log(newPedido);
      this.cliente = '';
      this.bordado = '';
    }
  }
}
