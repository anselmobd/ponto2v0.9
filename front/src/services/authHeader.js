import { useAuthStore } from '../stores/auth.js';

export function mountAuthHeader() {
  const auth = useAuthStore()
  if (auth?.user?.access) {
    return { Authorization: `Bearer ${auth.user.access}` };
  }
  return {};
}
  