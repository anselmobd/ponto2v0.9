import axios from 'axios'
import { slugify } from 'js/string.js'

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
          :disabled="!editing"
          @blur="blurCliente"
          @input="filterClientes"
          @dblclick="filterClientes"
          @keydown.down="inputClienteKeyDown"
          @keydown.up="inputClienteKeyUp"
          @keydown.enter="inputClienteKeyEnter"
          @keydown.tab="inputClienteKeyTab"
          type="text"
          id="cliente"
          ref="inputCliente"
          placeholder="Cliente"
        />
        <div
          class="custom-dropdown"
          :style="{ width: divDropdownWidth + 'px', left: divDropdownLeft + 'px' }"
          @mouseout="zeraOverCliente"
          ref="divDropdown"
        >
          <ul v-if="showClientesDropdown" ref="dropdownList">
            <li v-for="(cliente, index) in filteredClientes"
              :key="index"
              @mouseover="mouseoverCliente(cliente.apelido)"
              :class="{ 'selected': index === selectedClienteIndex }"
            >
              {{ cliente.apelido }}
            </li>
          </ul>
        </div>
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
      // variables of cliente dropdown functionallity
      clientes: [],
      filteredClientes: [],
      showClientesDropdown: false,
      selectedClienteIndex: -1,
      overCliente: '',
      divDropdownWidth: 0,
      divDropdownLeft: 0
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
          a => {
            return {
              apelido: a.apelido,
              slug: slugify(a.apelido)
            }
          }
        ).sort((a, b) => a.slug > b.slug);
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
    // methods of cliente dropdown functionallity
    mouseoverCliente(cliente) {
      this.overCliente = cliente;
    },
    zeraOverCliente() {
      this.overCliente = '';
    },
    blurCliente(event) {
      if (this.overCliente) {
        this.selectCliente(this.overCliente)
        this.zeraOverCliente();
      } else {
        this.showClientesDropdown = false
      }
    },
    filterClientes() {
      this.selectedClienteIndex = -1;
      this.filteredClientes = this.clientes.filter(c =>
        c.slug.includes(slugify(this.cliente))
        );
      this.showClientesDropdown = this.filteredClientes.length > 0;
    },
    selectCliente(cliente) {
      this.cliente = cliente;
      this.showClientesDropdown = false;
    },
    inputClienteKeyDown() {
      if (this.selectedClienteIndex < this.filteredClientes.length - 1) {
        this.selectedClienteIndex++;
        this.scrollToSelected();
      }
    },
    inputClienteKeyUp() {
      if (this.selectedClienteIndex > 0) {
        this.selectedClienteIndex--;
        this.scrollToSelected();
      }
    },
    inputClienteKeyEnter() {
      if (this.selectedClienteIndex == -1) {
        if (this.filteredClientes.length == 1) {
          this.selectCliente(this.filteredClientes[0].apelido);
          this.zeraOverCliente();
        }
      } else {
        this.selectCliente(this.filteredClientes[this.selectedClienteIndex].apelido);
        this.zeraOverCliente();
      }
    },
    inputClienteKeyTab() {
      this.zeraOverCliente();
    },
    scrollToSelected() {
      this.$nextTick(() => {
        const dropdownList = this.$refs.dropdownList;
        if (dropdownList && dropdownList.children[this.selectedClienteIndex]) {
          dropdownList.children[this.selectedClienteIndex].scrollIntoView({
            behavior: "auto",
            block: "nearest",
          });
        }
      });
    },
    setDivWidthLeft() {
      const inputElement = this.$refs.inputCliente;
      if (inputElement) {
        this.divDropdownWidth = inputElement.clientWidth;
        this.divDropdownLeft = inputElement.offsetLeft;
      }
    },
    inputClienteFocus() {
      this.$nextTick(() => {
        const inputElement = this.$refs.inputCliente;
        inputElement.focus();
      });
    },
    inputClienteNextFocus() {
      this.$nextTick(() => {
        const inputElement = this.$refs.inputClienteNext;
        inputElement.focus();
      });
    }
  },
  watch: {
    editing: function (value) {
      if (value) {
        this.inputClienteFocus();
      };
    },
    showClientesDropdown: function (value) {
      if (value) {
        this.setDivWidthLeft();
      } else {
        this.inputClienteNextFocus();
      };
    }
  }
}
