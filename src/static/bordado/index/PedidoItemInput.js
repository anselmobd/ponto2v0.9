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
          type="text"
          id="cliente"
          ref="inputCliente"
          placeholder="Cliente"
        />
        <div
          class="custom-dropdown"
          :style="{ width: divDropdownWidth + 'px', left: divDropdownLeft + 'px' }"
          @mouseout="zeraOverCliente"
        >
          <ul v-if="showClientesDropdown" ref="dropdownList">
            <li v-for="(cliente, index) in filteredClientes"
              :key="index"
              @mouseover="mouseoverCliente(cliente)"
              :class="{ 'selected': index === selectedIndex }"
            >
              {{ cliente }}
            </li>
          </ul>
        </div>
      </td>
      <td><input v-model.trim="bordado" :disabled="!editing" type="text" id="bordado" placeholder="Bordado"></td>
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
      clientes: ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7"],
      filteredClientes: [],
      showClientesDropdown: false,
      selectedIndex: -1,
      overCliente: '',
      divDropdownWidth: 0,
      divDropdownLeft: 0
    }
  },
  methods: {
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
        event.preventDefault();
        this.selectCliente(this.overCliente)
        this.zeraOverCliente();
        // this.inputClienteFocus();
      } else {
        this.showClientesDropdown = false
      }
    },
    filterClientes() {
      this.selectedIndex = -1;
      this.filteredClientes = this.clientes.filter((cliente) =>
        cliente.toLowerCase().includes(this.cliente.toLowerCase())
      );
      this.showClientesDropdown = this.filteredClientes.length > 0;
    },
    selectCliente(cliente) {
      this.cliente = cliente;
      this.showClientesDropdown = false;
    },
    inputClienteKeyDown() {
      if (this.selectedIndex < this.filteredClientes.length - 1) {
        this.selectedIndex++;
        this.scrollToSelected();
      }
    },
    inputClienteKeyUp() {
      if (this.selectedIndex > 0) {
        this.selectedIndex--;
        this.scrollToSelected();
      }
    },
    inputClienteKeyEnter() {
      if (this.selectedIndex == -1) {
        if (this.filteredClientes.length == 1) {
          this.selectCliente(this.filteredClientes[0]);  
        }
      } else {
        this.selectCliente(this.filteredClientes[this.selectedIndex]);
      }
    },
    scrollToSelected() {
      this.$nextTick(() => {
        const dropdownList = this.$refs.dropdownList;
        if (dropdownList && dropdownList.children[this.selectedIndex]) {
          dropdownList.children[this.selectedIndex].scrollIntoView({
            behavior: "auto",
            block: "nearest",
          });
        }
      });
    },
    setInputWidth() {
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
        this.setInputWidth();
      };
    }
  }
}
