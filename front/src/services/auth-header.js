import { useAuthStore } from '../stores/auth.js';

export default function authHeader() {
    const auth = useAuthStore()
    let user = auth.user;
  
    if (user && user.accessToken) {
      return { Authorization: 'Bearer ' + user.accessToken };
    } else {
      return {};
    }
  }
  