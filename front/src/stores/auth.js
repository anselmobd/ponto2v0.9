import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {
      name: ''
    },
  }),
  actions: {
    setUser(name, access, refresh) {
      this.user = {
        name: name,
        access: access,
        refresh: refresh,
      };
    },
    encerrar() {
      this.user = {
        name: '',
      };
    },
  }
})
