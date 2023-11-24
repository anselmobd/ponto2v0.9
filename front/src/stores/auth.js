import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {
      id: 1,
      name: 'anselmo'
    },
  }),
  actions: {
    setUser(user) {
      this.user = user;
    },
    encerrar() {
      this.user = {
        id: 0,
      };
    },
  }
})
