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
          @input="filterClientes"
          @blur="showClientesSuggestions = false"
          @keydown.down="moveDown"
          @keydown.up="moveUp"
          @keydown.enter="selectCurrentItem"
          type="text"
          id="cliente"
          ref="customInput"
          placeholder="Cliente"
        />
        <div class="custom-dropdown" :style="{ width: inputWidth + 'px', left: inputLeft + 'px' }">
        <ul v-if="showClientesSuggestions" ref="dropdownList">
          <li v-for="(cliente, index) in filteredClientes"
            :key="index"
            @click="selectCliente(cliente)"
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
      clientes: ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7"],
      filteredClientes: [],
      showClientesSuggestions: false,
      selectedIndex: -1,
      inputWidth: 0,
      inputLeft: 0
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
    filterClientes() {
      this.filteredClientes = this.clientes.filter((cliente) =>
        cliente.toLowerCase().includes(this.cliente.toLowerCase())
      );
      this.showClientesSuggestions = this.filteredClientes.length > 0;
    },
    selectCliente(cliente) {
      this.cliente = cliente;
      this.showClientesSuggestions = false;
    },
    moveDown() {
      if (this.selectedIndex < this.filteredClientes.length - 1) {
        this.selectedIndex++;
        this.scrollToSelected();
      }
    },
    moveUp() {
      if (this.selectedIndex > 0) {
        this.selectedIndex--;
        this.scrollToSelected();
      }
    },
    selectCurrentItem() {
      if (this.selectedIndex == -1) {
        if (this.filteredClientes.length == 1) {
          this.selectCliente(this.filteredClientes[0]);  
        }
      } else {
        this.selectCliente(this.filteredClientes[this.selectedIndex]);
      }
      this.selectedIndex = -1;
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
      const inputElement = this.$refs.customInput;
      if (inputElement) {
        this.inputWidth = inputElement.clientWidth;
        this.inputLeft = inputElement.offsetLeft;
      }
    }
  },
  watch: {
    editing: function (value) {
      if (value) {
        this.$nextTick(() => {
          document.getElementById("cliente").focus();
        });
      };
    },
    showClientesSuggestions: function (value) {
      if (value) {
        this.setInputWidth();
      };
    }
  }
}
