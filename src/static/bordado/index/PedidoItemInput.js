import axios from 'axios'


export default {
  props: [
    'editing'
  ],
  template:
    /*html*/
    `
    <tr class="input-row">
      <td>-</td>
      <td>
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
      </td>
      <td>
        <input
          v-model.trim="bordado"
          :disabled="!editing"
          type="text"
          id="bordado"
          placeholder="Bordado"
          ref="inputClienteNext"
        >
      </td>
      <td>
        <button :hidden="!editing" type="button" class="btn btn-primary me-2">Salva</button>
        <button @click="handleCancelaClick" :hidden="!editing" type="button" class="btn btn-primary me-2">Cancela</button>
        <button @click="handleNovoClick" :hidden="editing" type="button" class="btn btn-primary me-2">Novo</button>
      </td>
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
      clientes: []
    }
  },
  mounted() {
    this.GetClientes();
  },
  methods: {
    GetClientes() {
      axios.get('/bordado/api/clientes/?format=json')
      .then(response => {
        this.clientes = response.data.results.map(
          a => a.apelido
        ).sort();
      })
      .catch(error => {
        console.error('Erro ao obter clientes via API:', error);
      });
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
