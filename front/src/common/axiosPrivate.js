import { axiosPublic } from "./axiosPublic.js";
import { authHeader } from '../services/auth-header.js'

axiosPublic.interceptors.request.use(
  async (config) => {
    let auth_headers = authHeader();
    config.headers = {
      ...config.headers,
      ...auth_headers
    };
    return config;
  },
  (error) => Promise.reject(error)
);
