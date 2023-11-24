<template>
  <div>
    <h2 class="login__h2">Identificação</h2>
    <form class="login__form">
      <p class="login__p">
        <label class="login__label" for="username">Usuário:</label>
        <input class="login__input" type="text" name="username" id="username" placeholder="username" required>
      </p>
      <p class="login__p">
        <label class="login__label" for="password">Senha:</label>
        <input class="login__input" type="password" name="password" id="password" placeholder="password" required>
      </p>
      <button class="login__button" type="submit">Enviar</button>
    </form>
  </div>
</template>

<style scoped>
/* || CONTACT */

.login__h2 {
    margin: 0;
    font-weight: bold;
    font-size: larger;
}

.login__p {
    margin: 1em 0;
}

.login__label {
    display: block;
    font-weight: bold;
}

.login__input,
.login__textarea {
    padding: 0.5em;
    border-radius: 15px;
    border-width: 2px;
    width: 100%;
}

.login__button {
    padding: 0.5em;
    border-radius: 15px;
    background-color: rgb(52, 136, 161);
    color: whitesmoke;
    font-weight: bold;
}
</style>