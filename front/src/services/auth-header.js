import { useAuthStore } from '../stores/auth.js';

export default function authHeader() {
    const auth = useAuthStore()
    let user = auth.user;
  
    if (user && user.access) {
      return { Authorization: 'Bearer ' + user.access };
    } else {
      return {};
    }
  }
  