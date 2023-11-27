// import mem from "mem";
import { useAuthStore } from '../stores/auth.js';
import { axiosPublic } from "./axiosPublic";


export const refreshAccessToken = async () => {
  console.log('refreshJwt');
  const auth = useAuthStore()

  const params = new URLSearchParams();
  params.append('format', 'json');
  console.log(params);

  const { setUser, encerrar } = auth

  var result = 0;

  console.log('antes do try');
  try {
    const response = await axiosPublic.post(
      "/api/token/refresh/",
      {refresh: auth.user.refresh},
      {params: params}
    );
    console.log('refreshJwt then');
    console.log('response', response);

    if (response?.data?.access) {
      console.log('get new access');
      setUser(
        auth.user.name,
        response.data.access,
        auth.user.refresh
      );
      console.log('user setado');
    } else {
      console.log('do not get new access');
      encerrar();
    }
    console.log('pos if');
    result = response.status;
    console.log('result', result);
    console.log('fim do try');
  } catch (error) {
    console.log('refreshJwt catch');
    console.error(error);
    encerrar();
    result = error.response.status;
    console.log('fim do catch');
  }
  console.log('depois do try catch');
  return result;
};
