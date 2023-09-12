export default {
  template:
    /*html*/
    `
    <tr class="input-row">
      <td>-</td>
      <td><input v-model.trim="cliente" :disabled="!editing" type="text" id="cliente" placeholder="Cliente"></td>
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
      editing: false,
      cliente: '',
      bordado: '',
      error: {
        cliente: '',
        bordado: ''
      }
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
      this.editing = true;
    },
    handleCancelaClick(event) {
      event.preventDefault();
      this.clearInputs();
      this.editing = false;
    }
  },
  watch: {
    editing: function (value) {
      if (value) {
        this.$nextTick(() => {
          document.getElementById("cliente").focus();
        });
      };
    }
  }
}
