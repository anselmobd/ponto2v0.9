import axios from "axios";
import { mountAuthHeader } from '../services/authHeader.js'
import { refreshAccessToken } from '../services/refreshToken.js';


export const axiosPrivate = axios.create({
  baseURL: "http://tt.o2:8902",
  headers: {
    "Content-Type": "application/json",
  },
  xsrfHeaderName: "X-CSRFTOKEN",
  xsrfCookieName: "csrftoken"
});



axiosPrivate.interceptors.request.use(
  async (config) => {
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
    const config = error?.config;

    if (error?.response?.status === 401 && !config?.sent) {
      config.sent = true;

      const result = await refreshAccessToken();
      if (result == 200) {
        let auth_headers = mountAuthHeader();
        config.headers = {
          ...config.headers,
          ...auth_headers
        };
        return axios(config);
      }
    }
    return Promise.reject(error);
  }
);
