import { useAuthStore } from '../stores/auth.js';
import { axiosPublic } from "../common/axiosPublic.js";

export const refreshAccessToken = async () => {
  const params = new URLSearchParams();
  params.append('format', 'json');
  
  const auth = useAuthStore()
  const { setUser, encerrar } = auth

  var result = 0;
  try {
    const response = await axiosPublic.post(
      "/api/token/refreshh/",
      {refresh: auth.user.refresh},
      {params: params}
    );

    if (response?.data?.access) {
      setUser(
        auth.user.name,
        response.data.access,
        auth.user.refresh
      );
    } else {
      encerrar();
    }
    result = response.status;
  } catch (error) {
    encerrar();
    result = error.response.status;
  }
  return result;
};
