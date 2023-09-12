export default {
  props: [
    'pedido_item',
    'editing'
  ],
  template:
    /*html*/
    `
    <tr>
      <td>{{pedidoItemInseridoEmData(pedido_item)}}</td>
      <td>{{pedido_item.pedido.cliente.apelido}}</td>
      <td>{{pedido_item.bordado.nome}}</td>
      <td>
        <button :disabled="editing" class="btn">Editar</button>
        <button :disabled="editing" class="btn">Apagar</button>
      </td>
    </tr>
    `,
  data() {
    return {}
  },
  methods: {
    pedidoItemInseridoEmData(pedido_item) {
      var date = new Date(pedido_item.inserido_em)
      return date.toLocaleDateString('pt-br');
    }
  }
}
