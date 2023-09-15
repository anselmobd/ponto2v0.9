import axios from 'axios'


export default {
  props: [
    'editing'
  ],
  template:
    /*html*/
    `
    <tr class="input-row">
      <th>-</th>
      <th>
        <input
          v-model.trim="cliente"
          list="clientes-list"
          :disabled="!editing"
          type="text"
          ref="inputCliente"
          placeholder="Cliente"
        >
        <datalist id="clientes-list">
          <option v-for="cliente in clientes">{{cliente}}</option>
        </datalist>
      </th>
      <th>
        <input
          v-model.trim="bordado"
          list="bordados-list"
          :disabled="!editing"
          @focus="GetBordados"
          type="text"
          id="bordado"
          placeholder="Bordado"
        >
        <datalist id="bordados-list">
          <option v-for="bordado in bordados">{{bordado}}</option>
        </datalist>
      </th>
      <th>
        <button @click="handleSalvaClick" :hidden="!editing" type="button" class="btn btn-primary me-2">Salva</button>
        <button @click="handleCancelaClick" :hidden="!editing" type="button" class="btn btn-primary me-2">Cancela</button>
        <button @click="handleNovoClick" :hidden="editing" type="button" class="btn btn-primary me-2">Novo</button>
      </th>
    </tr>
    `,
  data() {
    return {
      cliente: '',
      bordado: '',
      error: {
        cliente: '',
        bordado: ''
      },
      clientes: [],
      bordados: [],
      new_cliente: {}
    }
  },
  mounted() {
    this.GetClientes();
  },
  methods: {
    GetClientes() {
      const params = new URLSearchParams();
      params.append('format', 'json');
      axios.get('/bordado/api/clientes/', {params: params})
      .then(response => {
        this.clientes = response.data.results.map(
          a => a.apelido
        );
      })
      .catch(error => {
        console.error('Erro ao obter clientes via API:', error);
      });
    },
    SetCliente() {
      let cliente_existe = this.clientes.includes(this.cliente);
      if (!cliente_existe) {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        const params = new URLSearchParams();
        params.append('format', 'json');
        axios.post(
          '/bordado/api/clientes/',
          {
            apelido: this.cliente,
          },
          {params: params},
        )
        .then(response => {
          this.new_cliente = response.data.results;
        })
        .catch(error => {
          console.error('Erro ao criar novo cliente via API:', error);
        });
      }
    },
    GetBordados() {
      if (this.cliente) {
        const params = new URLSearchParams();
        params.append('format', 'json');
        params.append('cliente__apelido', this.cliente);
        axios.get('/bordado/api/bordado/', {params: params})
        .then(response => {
          this.bordados = response.data.results.map(
            a => a.nome
          );
        })
        .catch(error => {
          console.error('Erro ao obter clientes via API:', error);
        });
      } else {
        this.bordados = [];
      }
    },
    clearInputs() {
      this.cliente = '';
      this.bordado = '';
    },
    handleNovoClick(event) {
      event.preventDefault();
      this.clearInputs();
      this.$emit('pedido-item-editing', true);
    },
    handleSalvaClick(event) {
      this.SetCliente();
    },
    handleCancelaClick(event) {
      event.preventDefault();
      this.clearInputs();
      this.$emit('pedido-item-editing', false);
    },
    inputClienteFocus() {
      this.$nextTick(() => {
        this.$refs.inputCliente.focus();
      });
    }
  },
  watch: {
    editing: function (value) {
      if (value) {
        this.inputClienteFocus();
      };
    }
  }
}
