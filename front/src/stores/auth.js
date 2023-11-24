import { defineStore } from 'pinia'
import VueCookies from 'vue-cookies'

var saved_user = VueCookies.get('user');
if (! saved_user) {
  saved_user = {
    name: ''
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: saved_user,
  }),
  actions: {
    setUser(name, access, refresh) {
      this.user = {
        name: name,
        access: access,
        refresh: refresh,
      };
      VueCookies.set('user', this.user, "24h");
    },
    encerrar() {
      this.user = {
        name: '',
      };
      VueCookies.remove('user');
    },
  }
})
