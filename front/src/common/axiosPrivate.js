import axios from "axios";
import { mountAuthHeader } from '../services/auth-header.js'
import { refreshAccessToken } from '../services/refreshToken.js';


export const axiosPrivate = axios.create({
  baseURL: "http://tt.o2:8902",
  headers: {
    "Content-Type": "application/json",
  },
});

axiosPrivate.interceptors.request.use(
  async (config) => {
    console.log('interceptors.request')
    console.log('config', config)
    let auth_headers = mountAuthHeader();
    config.headers = {
      ...config.headers,
      ...auth_headers
    };
    return config;
  },
  (error) => Promise.reject(error)
);

axiosPrivate.interceptors.response.use(
  (response) => response,
  async (error) => {
    console.log('interceptors.response error')
    const config = error?.config;
    console.log('config', config)
    console.log('error?.response?.status', error?.response?.status)
    console.log('config?.sent', config?.sent)

    if (error?.response?.status === 401 && !config?.sent) {
      console.log('interceptors.response entrou no if')

      config.sent = true;

      // const result = await memoizedRefreshToken();
      const result = await refreshAccessToken();

      // if (result?.accessToken) {
      if (result == 200) {
        // config.headers = {
        //   ...config.headers,
        //   authorization: `Bearer ${result?.accessToken}`,
        // };
        let auth_headers = mountAuthHeader();
        config.headers = {
          ...config.headers,
          ...auth_headers
        };
      }

      return axios(config);
    }
    return Promise.reject(error);
  }
);
