import { axiosPublic } from "./axiosPublic.js";
import { authHeader } from '../services/auth-header.js'

export const axiosPrivate = axiosPublic;
console.log('axiosPrivate', axiosPrivate);

axiosPrivate.interceptors.request.use(
  async (config) => {
    console.log('interceptors.request')
    console.log('config', config)
    let auth_headers = authHeader();
    config.headers = {
      ...config.headers,
      ...auth_headers
    };
    return config;
  },
  (error) => Promise.reject(error)
);
