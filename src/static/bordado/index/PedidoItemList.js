export default {
  props: [
    'pedido_item'
  ],
  template:
    /*html*/
    `
    <tr>
      <td>{{pedidoItemInseridoEmData(pedido_item)}}</td>
      <td>{{pedido_item.pedido.cliente.apelido}}</td>
      <td>{{pedido_item.bordado.nome}}</td>
      <td>
        <button :disabled="executando_acao" class="btn">Editar</button>
        <button :disabled="executando_acao" class="btn">Apagar</button>
      </td>
    </tr>
    `,
  data() {
    return {
      executando_acao: false
    }
  },
  methods: {
    pedidoItemInseridoEmData(pedido_item) {
      var date = new Date(pedido_item.inserido_em)
      return date.toLocaleDateString('pt-br');
    }
  }
}
