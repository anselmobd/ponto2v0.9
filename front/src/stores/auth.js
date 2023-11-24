import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {
      id: 1,
      name: 'anselmo'
    },
  }),
  actions: {
    encerrar() {
      this.user = {
        id: 0,
      };
    },
  }
})
