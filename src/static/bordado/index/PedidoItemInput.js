import axios from 'axios'


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


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
        <span v-if="error.cliente"><span class="input-error-msg">{{ error.cliente }}</span><br/></span>
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
        <span v-if="error.bordado"><span class="input-error-msg">{{ error.bordado }}</span><br/></span>
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
    }
  },
  mounted() {
    this.GetClientes();
  },
  methods: {
    GetClientes() {
      const params = new URLSearchParams();
      params.append('format', 'json');
      params.append('page_size', '999999');
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
    SetClienteBordado(afterSet) {
      const params = new URLSearchParams();
      params.append('format', 'json');
      axios.post(
        '/bordado/api/pedido_item/',
        {
          cliente: {
            apelido: this.cliente
          },
          bordado: {
            nome: this.bordado
          },
        },
        {params: params},
      )
      .then(response => {
        afterSet(true, response.data);
      })
      .catch(error => {
        console.error('Erro ao gravar cliente / bordado via API:', error);
        afterSet(false, error.response.data);
      });
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
      this.$emit('pedido-item-inserting');
    },
    handleSalvaClick(event) {
      for(const key in this.error)
        this.error[key] = '';
      this.SetClienteBordado(this.afterSalvaSet);
    },
    afterSalvaSet(ok, data) {
      if (ok) {
        this.$emit('pedido-item-para-tela', data);
        this.clearInputs();
      } else {
        if ('apelido' in data) {
          this.error.cliente = data.apelido.join('|');
        }
        if ('nome' in data) {
          this.error.bordado = data.nome.join('|');
        }
      };
      this.GetClientes();
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
