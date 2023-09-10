import axios from 'axios'

export default {
  template:
    /*html*/
    `
    <h3>Clientes</h3>
    <ul>
      <li  v-for="cliente in clientes" :key="cliente.id">
        {{ cliente.apelido }}
      </li>
    </ul>
    `,
  data() {
    return {
      clientes: {}
    }
  },
  mounted() {
    axios.get('/bordado/api/clientes/?format=json')
    .then(response => {
      this.clientes = response.data;
    })
    .catch(error => {
      console.error('Erro ao obter clientes via API:', error);
    });
  }
}
