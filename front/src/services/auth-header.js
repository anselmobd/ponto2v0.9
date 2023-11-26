import { useAuthStore } from '../stores/auth.js';

export function authHeader() {
  const auth = useAuthStore()
  if (auth?.user?.access) {
    return { Authorization: 'Bearer ' + auth.user.access };
  }
  return {};
}
  